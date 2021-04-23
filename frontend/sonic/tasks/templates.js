
const { patchPipe } = require('../utilities/handle-errors.js')
const paths = require('../paths.js')
const { dest, src } = require('vinyl-fs')
const { apply, changed, replace } = require('@eklingen/vinyl-stream-gears')
const nunjucks = require('@eklingen/vinyl-stream-nunjucks')

/* START NUNJUCKS LISTENERS PATCH */
require('events').EventEmitter.defaultMaxListeners = 100 // Amount of expected templates
/* END NUNJUCKS LISTENERS PATCH */

// Compile templates from source to destination
function templates () {
  const nunjucksConfig = require('../../config/nunjucks')({ env: global.buildEnv })

  global.templateCount = 0

  let stream = src(paths.templates.sourceGlobs).pipe(patchPipe())

  stream = stream.pipe(nunjucks(nunjucksConfig))
  stream = stream.pipe(replace(
    global.buildEnv === 'production' ? [
      { replace: /[\u2028]/gi, value: '' }, // Replace weird characters
      { replace: /^\s+$/gm, value: '\n' }, // Replace whitespace/newlines with a single newline
      { replace: /\n+/gm, value: '\n' }, // Replace multiple newlines with a single newline
      { replace: /<style([\S\s]*?)>([\S\s]*?)<\/style>/gm, value: str => str.replace(/\s+/gm, ' ') }, // Style innards on one line
      { replace: /<script([\S\s]*?)>([\S\s]*?)<\/script>/gm, value: str => str.replace(/\s+/gm, ' ') } // Script innards on one line
    ] : []
  ))
  stream = stream.pipe(changed(paths.templates.destinationPath, { method: 'contents' }))
  stream = stream.pipe(apply(() => { global.templateCount++ }))
  stream = stream.pipe(dest(paths.templates.destinationPath))

  stream = stream.on('finish', () => {
    console.log(`     `, global.templateCount, `templates generated`)
  })

  return stream
}

module.exports = templates
