
const config = require('../../config/sonic.js')
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../paths.js')
const { src } = require('vinyl-fs')
const { run } = require('@eklingen/vinyl-stream-gears')

// Sync build directory to staging -- NOTE: No error handler due to lack of a vinyl stream.
function sync () {
  let stream = src('.', { read: false }).pipe(patchPipe())

  stream = stream.pipe(run(`rsync -rLktzi --safe-links --delete --quiet --exclude=".*" -e ssh ./${paths.project.destinationPath}/ ${config.staging.user}@${config.staging.ip}:${config.staging.path}`))

  return stream
}

module.exports = sync
