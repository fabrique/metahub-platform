// Profiler. Writes a file to disk that you can then open in Chrome inspector.
// Copy pasted from https://github.com/filipesilva/terser-performance

const { promisify } = require('util')
const fs = require('fs')
const inspector = require('inspector')
const path = require('path')

const DEFAULT_OPTIONS = {
  type: 'cpu', // or: 'heap' or 'heap-snapshot',
  interval: 1 * 1000
}

// Call fn after interval ms, wait for it to finish, then repeat.
// Returns a callback that calls fn one last time and stops repeating.
const rollingTimeout = (fn, interval) => {
  let lastTimeout

  const chainedTimeout = () => {
    lastTimeout = setTimeout(async () => {
      await fn()
      chainedTimeout()
    }, interval)
  }

  chainedTimeout()

  const stopCb = async () => {
    clearTimeout(lastTimeout)
    await fn()
  }

  return stopCb
}

let before = async () => { }
let after = async () => { }

// No colons ISO format, suitable for filenames.
const init = async (fn, options = {}) => {
  options = { ...DEFAULT_OPTIONS, ...options }

  const basicISONow = () => new Date().toISOString().replace(/[-.:]/g, '')
  const session = new inspector.Session()

  // Adding a method because of https://github.com/nodejs/node/issues/13338#issuecomment-307165905.
  session.postPromise = promisify(session.post)
  session.connect()

  const sampleInterval = 500

  if (options.type === 'cpu') {
    console.log('🕵️‍   Taking cpu profile...')

    before = async () => {
      await session.postPromise('Profiler.enable')
      await session.postPromise('Profiler.start')
    }

    after = async () => {
      const { profile } = await session.postPromise('Profiler.stop')
      fs.writeFileSync(path.resolve(process.cwd(), `__${basicISONow()}.cpuprofile`), JSON.stringify(profile))
    }
  } else if (options.type === 'heap') {
    console.log('🕵️‍   Taking heap profile...')

    const writeHeapProfile = async () => {
      const { profile } = await session.postPromise('HeapProfiler.getSamplingProfile')
      fs.writeFileSync(path.resolve(process.cwd(), `__${basicISONow()}.heapprofile`), JSON.stringify(profile))
    }

    let stopCb
    before = async () => {
      await session.postPromise('HeapProfiler.enable')
      await session.postPromise('HeapProfiler.startSampling')
      stopCb = rollingTimeout(writeHeapProfile, sampleInterval)
    }
    after = async () => stopCb()
  } else if (options.type === 'heap-snapshot') {
    console.log('🕵️‍   Taking heap snapshot...')

    const writeHeapSnapshot = async () => {
      const fd = fs.openSync(path.resolve(process.cwd(), `__${basicISONow()}.heapsnapshot`), 'w')

      session.on('HeapProfiler.addHeapSnapshotChunk', (m) => {
        fs.writeSync(fd, m.params.chunk)
      })

      await session.postPromise('HeapProfiler.writeHeapSnapshot')
      fs.closeSync(fd)
    }

    let stopCb
    before = async () => {
      stopCb = rollingTimeout(writeHeapSnapshot, sampleInterval)
    }
    after = async () => stopCb()
  }
}

const start = async () => {
  await before()
}
const stop = async () => {
  await after()
}

module.exports = { init, start, stop }
