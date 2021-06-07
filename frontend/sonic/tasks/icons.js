
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../../config/sonic.paths.js')
const { dest, src } = require('vinyl-fs')
const { apply, changedInPlace } = require('@eklingen/vinyl-stream-gears')
const optimizeImages = require('@eklingen/vinyl-stream-optimize-images')

// Compress icons in source; for includes and such
function icons () {
  const optimizeImagesConfig = require('../../config/optimize-images')

  global.iconsCounter = 0

  let stream = src(paths.icons.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changedInPlace.filter(paths.icons.sourcePath)) // Ignore unchanged files in place using a cache file
  stream = stream.pipe(optimizeImages(optimizeImagesConfig)) // Optimize images
  stream = stream.pipe(apply(() => { global.iconsCounter++ }))
  stream = stream.pipe(dest(file => file.base)) // Write back to source

  stream = stream.on('finish', () => {
    console.log('     ', global.iconsCounter, 'icons optimized')
    changedInPlace.remember(paths.icons.sourcePath) // Save cache file for next time
  })

  return stream
}

module.exports = icons
