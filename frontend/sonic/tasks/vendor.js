
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../../config/sonic.paths.js')
const { dest, src, symlink } = require('vinyl-fs')
const { changed, apply } = require('@eklingen/vinyl-stream-gears')

// Symlink vendor assets from source to destination
function vendor () {
  global.vendorCounter = 0

  let stream = src(paths.vendor.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changed(paths.vendor.destinationpath, { method: 'exists ' }))
  stream = stream.pipe(apply(() => { global.vencorCounter++ }))
  stream = stream.pipe(global.useSymlinks ? symlink(paths.vendor.destinationPath, { overwrite: true }) : dest(paths.vendor.destinationPath))

  stream = stream.on('finish', () => {
    console.log('     ', global.vendorCounter, 'vendor files', global.useSymlinks ? 'symlinked' : 'copied')
  })

  return stream
}

module.exports = vendor
