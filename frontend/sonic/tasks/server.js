
const config = require('../../config/sonic.js')
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../../config/sonic.paths.js')
const { src } = require('vinyl-fs')
const connect = require('@eklingen/vinyl-stream-connect')

// Start serving the build directory over http
function server (callback) {
  console.log(`❯   \x1b[34mServing\x1b[0m on \x1b[36;4mhttp://${config.server.host}:${config.server.port}\x1b[0m`, config.server.liveReload ? '\x1b[2m(LiveReload enabled)\x1b[0m' : '')

  let stream = src(paths.project.destinationPath, { read: false }).pipe(patchPipe())

  stream = stream.pipe(connect({ ...config.server, log: global.verboseOutput ? 'verbose' : 'quiet' }))

  return stream
}

module.exports = server
