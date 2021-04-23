// Glob loader
// Based on: https://github.com/Aintaer/import-glob-loader
// Reasons for changes:
// - Fixed webpack 4 compatibility
// - Added support for require() calls as well
// - Removed loader-utils dependency

const { hasMagic, sync } = require('glob')

function importGlob (source) {
  const options = { nodir: true, cwd: this.context }
  const { test = '(import|require)', delimiter = '\n' } = options
  const qualifier = new RegExp(`^.*\\b${test}\\b(.*)$`, 'gm')

  function expandGlob (result) {
    if (!result) {
      return
    }

    const [match, quote, content] = result
    const offset = result.index
    const line = result.input

    if (!hasMagic(content)) {
      return
    }

    const pre = line.slice(0, offset)
    const post = line.slice(offset + match.length)

    return sync(content, options).map(filename => `${pre}${quote}${filename}${quote}${post}`).join(delimiter)
  }

  const quotedString = /(['"])(.*?)\1/

  function expandLine (line, payload) {
    if (!(payload && payload.trim())) {
      return line
    }

    return expandGlob(quotedString.exec(line)) || line
  }

  return source.replace(qualifier, expandLine)
}

module.exports = { importGlob }
module.exports.default = importGlob
