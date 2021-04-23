
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../paths.js')
const { dest, src } = require('vinyl-fs')
const { changed, filesize, replace } = require('@eklingen/vinyl-stream-gears')
const webpack = require('@eklingen/vinyl-stream-webpack')
const eslint = require('@eklingen/vinyl-stream-eslint')

// Compile scripts from source to destination
function scripts () {
  const webpackConfig = require('../../config/webpack.js')({ mode: global.buildEnv, src: paths.project.sourcePath })

  let stream = src(paths.scripts.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(webpack({ config: webpackConfig }))
  // stream = stream.pipe(replace([{ replace: /(webpack:\/\/\/)+/gm, value: '' }])) // Work around bug in Webpack v5
  stream = stream.pipe(changed(paths.scripts.destinationPath, { method: 'contents' })) // Ignore unchanged files
  stream = stream.pipe(dest(paths.scripts.destinationPath))
  stream = stream.pipe(filesize()) // Show gzipped file size in console

  return stream
}

// Lint scripts from source
function lintScripts () {
  const eslintConfig = require('../../config/eslint.web.js')

  let stream = src(paths.scripts.lintGlobs, { read: false }).pipe(patchPipe())

  stream = stream.pipe(eslint({ config: eslintConfig, files: paths.scripts.lintGlobs })) // Lint files with .eslint settings (and autofix, if possible)

  return stream
}

module.exports = scripts
module.exports.lint = lintScripts
