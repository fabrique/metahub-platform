// Intercept require() calls for testing
// Prints 'em out all pretty like with loadtime in ms.
// Also; any duration above 'small' is red, and anything above 'large' is red and bright.

// TODO: Made some preparations to cache the output, so it can be a nicely formatted tree instead of a giant list
const path = require('path')
const Module = require('module')

function truncatePath (filePath) {
  const root = process.cwd()

  // Strip cwd from path
  const rootIndex = filePath.indexOf(root)
  if (rootIndex !== -1) {
    filePath = filePath.substr(rootIndex + root.length, filePath.length - (rootIndex + root.length))
  }

  // Strip preceding slash
  if (filePath[0] === '/') {
    filePath = filePath.substr(1, filePath.length - 1)
  }

  return filePath
}

function unflatten (array = [], parent = { filename: '' }, isRoot = false) {
  const children = array.filter(item => item.parentFilename === parent.filename)

  let tree = []

  if (!children.length) {
    return tree
  }

  if (isRoot) {
    tree = children
  } else {
    parent.children = children

    children.forEach(child => {
      Object.defineProperty(child, 'parent', {
        get: function () {
          return parent
        }
      })
    })
  }

  children.forEach(child => unflatten(array, child, false))

  return tree
}

function getPrefix (item, level = 0, prefix = '') {
  if (!level) {
    return prefix
  }

  let currentLevel = level
  let currentItem = item

  while (currentLevel) {
    if (currentItem.parent.children && currentItem.parent.children.length > 1) {
      if (currentItem === item) {
        if (currentItem.parent.children.indexOf(currentItem) === currentItem.parent.children.length - 1) {
          prefix = ' └─ ' + prefix
        } else {
          prefix = ' ├─ ' + prefix
        }
      } else {
        if (currentItem.parent.children.indexOf(currentItem) === currentItem.parent.children.length - 1) {
          prefix = '    ' + prefix
        } else {
          prefix = ' │  ' + prefix
        }
      }
    } else {
      if (currentItem === item) {
        prefix = ' └─ ' + prefix
      } else {
        prefix = '    ' + prefix
      }
    }

    currentLevel--
    currentItem = currentItem.parent
  }

  return prefix
}

module.exports = function traceRequire (cutoff = -1, sizeStep = 100) {
  const ORIGINAL_REQUIRE = Module.prototype.require
  const entries = []

  function printResults () {
    console.log('Dimensionalizing interflux ultrapositions...')

    const mainFilePath = path.relative(process.cwd(), require.main.filename || process.mainModule.filename)
    const parent = { filename: mainFilePath, elapsed: -1, parentFilename: '', count: 1 }
    const tree = unflatten(entries, parent, true)

    tree.forEach(item => printLine(item, 0))
  }

  function printLine (item, level = 0) {
    const colors = { green: '\x1b[32m', yellow: '\x1b[33m', red: '\x1b[31m', white: '\x1b[37m', bright: '\x1b[1m', reset: '\x1b[0m' }

    const result = `${item.elapsed.toString().padStart(5)} ms  `
    const filename = item.filename
    const count = (item.count > 1) ? `(${item.count}x)` : ''
    const prefix = getPrefix(item, level)
    const startColor = (item.elapsed >= sizeStep * 2) ? colors.red : (item.elapsed >= sizeStep) ? colors.yellow : colors.white

    console.log(`${startColor}${result}${colors.reset}`, `${prefix}${startColor}${filename}${colors.reset}`, count)

    if (item.children) {
      item.children.forEach(item => printLine(item, level + 1))
    }
  }

  Module.prototype.require = function (id) {
    const start = process.hrtime()
    const response = ORIGINAL_REQUIRE.call(this, id)
    const end = process.hrtime(start)
    const elapsed = Math.round((end[0] * 1000) + (end[1] / 1e6))

    // Using full filenames instead of id's (since they can be relative)
    const filename = truncatePath(this.filename)
    const parentFilename = truncatePath(this.parent ? this.parent.filename : '')

    const existingIndex = entries.findIndex(item => item.filename === filename)

    if (existingIndex !== -1) {
      entries[existingIndex].elapsed += elapsed
      entries[existingIndex].count += 1
    } else {
      if (elapsed > cutoff) {
        entries.push({ filename: filename, elapsed: elapsed, parentFilename: parentFilename, count: 1 })
      }
    }

    return response
  }

  process.on('exit', () => printResults())
}
