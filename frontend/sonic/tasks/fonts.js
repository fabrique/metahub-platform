
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../paths.js')
const { src, symlink } = require('vinyl-fs')
const { changed, apply } = require('@eklingen/vinyl-stream-gears')

// Symlink fonts from source to destination
function fonts () {
  global.fontsCounter = 0

  let stream = src(paths.fonts.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changed(paths.fonts.destinationpath, { method: 'exists ' }))
  stream = stream.pipe(symlink(paths.fonts.destinationPath, { overwrite: true })) // Symlink to destination
  stream = stream.pipe(apply(() => { global.fontsCounter++ }))

  stream = stream.on('finish', () => {
    console.log(`     `, global.fontsCounter, `fonts symlinked`)
  })

  return stream
}

module.exports = fonts
