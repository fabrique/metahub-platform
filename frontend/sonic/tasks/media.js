
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../paths.js')
const { dest, src, symlink } = require('vinyl-fs')
const { changedInPlace, changed, apply } = require('@eklingen/vinyl-stream-gears')
const optimizeImagesWrapper = require('@eklingen/vinyl-stream-optimize-images')

// Symlink media from source to destination
function media () {
  global.mediaCounter = 0

  let stream = src(paths.media.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changed(paths.media.destinationpath, { method: 'exists ' }))
  stream = stream.pipe(apply(() => { global.mediaCounter++ }))
  stream = stream.pipe(symlink(paths.media.destinationPath, { overwrite: true })) // Symlink to destination

  stream = stream.on('finish', () => {
    console.log(`     `, global.mediaCounter, `media files symlinked`)
  })

  return stream
}

// Optimize media in source
function optimizeMedia () {
  const optimizeImagesConfig = require('../../config/optimize-images')

  global.optimizeMediaCounter = 0

  let stream = src(paths.media.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(changedInPlace.filter(paths.media.sourcePath)) // Ignore unchanged files in place using a cache file
  stream = stream.pipe(optimizeImagesWrapper(optimizeImagesConfig)) // Optimize images
  stream = stream.pipe(apply(() => { global.optimizeMediaCounter++ }))
  stream = stream.pipe(dest(paths.media.sourcePath)) // Write to destination

  stream = stream.on('finish', () => {
    console.log(`     `, global.optimizeMediaCounter, `media files optimized`)
    changedInPlace.remember(paths.media.sourcePath) // Save cache file for next time
  })

  return stream
}

module.exports = media
module.exports.optimize = optimizeMedia
