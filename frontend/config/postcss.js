// PostCSS configuration

module.exports = (api) => {
  const plugins = []
  const options = {}

  // Autoprefixer
  const autoprefixer = require('autoprefixer')
  plugins.push(autoprefixer({ cascade: true, add: true, remove: true, supports: true, flexbox: true, grid: false }))

  // NOTE: This destroys source-maps. Gotta figure out why.
  // const { join } = require('path')
  // if (api.env === 'production') {
  //  const postcss = require('postcss')
  //  const cleanCSS = require(join(process.cwd(), 'sonic/plugins/postcss/clean-css'))
  //  plugins.push(cleanCSS({ level: 2, format: 'keep-breaks', specialComments: false }))
  // }

  return { plugins, options }
}
