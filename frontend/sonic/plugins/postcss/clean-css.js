// Clean CSS PostCSS plugin
// NOTE: Untested. Should be faster then running CleanCSS separately.
// This is theoretically because the AST has already been generated.

const { plugin, parse } = require('postcss')
const CleanCSS = require('clean-css')
const instance = new CleanCSS(options)

module.exports = plugin('clean', (options = {}) => {
  return (css, res) => new Promise((resolve, reject) => {
    const callback = (err, min) => {
      if (err) {
        return reject(new Error(err.join('\n')))
      }

      for (const w of min.warnings) {
        res.warn(w)
      }

      res.root = parse(min.styles)
      resolve()
    }

    instance.minify(css.toString(), callback)
  })
})
