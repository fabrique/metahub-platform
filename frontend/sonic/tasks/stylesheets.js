// Stylesheet related tasks

const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../paths.js')
const { dest, src } = require('vinyl-fs')
const { changed, prepend, filesize, log } = require('@eklingen/vinyl-stream-gears')
const unglob = require('@eklingen/vinyl-stream-unglob')
const postcss = require('@eklingen/vinyl-stream-postcss')
const sass = require('@eklingen/vinyl-stream-sass')
const stylelint = require('@eklingen/vinyl-stream-stylelint')

// Compile stylesheets from source to destination
function stylesheets () {
  const postcssConfig = require('../../config/postcss.js')({ env: global.buildEnv })
  const sassConfig = require('../../config/sass.js')({ env: global.buildEnv })

  let stream = src(paths.stylesheets.sourceGlobs, { sourcemaps: true }).pipe(patchPipe())

  stream = stream.pipe(prepend(`$ENV: '${global.buildEnv}';`)) // Insert variable0
  stream = stream.pipe(unglob({ sort: 'a-z', magicExtension: true })) // Enable @import globs
  stream = stream.pipe(sass({ sass: { includePaths: ['node_modules'], ...sassConfig }, tryBinary: false })) // TODO: BUG WITH BINARY DEBUG OUTPUT NOT SHOWING!
  stream = stream.pipe(postcss({ postcss: postcssConfig }))
  stream = stream.pipe(changed(paths.stylesheets.destinationPath, { method: 'contents', injectSourceMapComment: true }))
  stream = stream.pipe(dest(paths.stylesheets.destinationPath, { sourcemaps: '.' }))
  stream = stream.pipe(filesize())

  return stream
}

// Lint stylesheets from source
function lintStylesheets () {
  const stylelintConfig = require('../../config/stylelint.js')

  let stream = src(paths.stylesheets.lintGlobs, { read: true }).pipe(patchPipe())

  stream = stream.pipe(stylelint({ stylelint: { config: stylelintConfig, files: paths.stylesheets.lintGlobs, fix: true } }))

  return stream
}

module.exports = stylesheets
module.exports.lint = lintStylesheets
