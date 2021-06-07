
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../../config/sonic.paths.js')
const { dest, src, symlink } = require('vinyl-fs')
const { changedInPlace, changed, apply } = require('@eklingen/vinyl-stream-gears')
const optimizeImagesWrapper = require('@eklingen/vinyl-stream-optimize-images')

// Symlink images from source to destination
function images () {
  global.imagesCounter = 0

  let stream = src(paths.images.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changed(paths.images.destinationpath, { method: 'exists ' }))
  stream = stream.pipe(apply(() => { global.imagesCounter++ }))
  stream = stream.pipe(global.useSymlinks ? symlink(paths.images.destinationPath, { overwrite: true }) : dest(paths.images.destinationPath))

  stream = stream.on('finish', () => {
    console.log('     ', global.imagesCounter, 'images', global.useSymlinks ? 'symlinked' : 'copied')
  })

  return stream
}

// Optimize images in source
function optimizeImages () {
  const optimizeImagesConfig = require('../../config/optimize-images')

  global.optimizeImagesCounter = 0

  let stream = src(paths.images.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changedInPlace.filter(paths.images.sourcePath)) // Ignore unchanged files in place using a cache file
  stream = stream.pipe(optimizeImagesWrapper(optimizeImagesConfig)) // Optimize images
  stream = stream.pipe(apply(() => { global.optimizeImagesCounter++ }))
  stream = stream.pipe(dest(paths.images.sourcePath))

  stream = stream.on('finish', () => {
    console.log('     ', global.optimizeImagesCounter, 'images optimized')
    changedInPlace.remember(paths.images.sourcePath) // Save cache file for next time
  })

  return stream
}

module.exports = images
module.exports.optimize = optimizeImages
