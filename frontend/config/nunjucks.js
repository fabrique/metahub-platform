// Nunjucks configuration

module.exports = function (api) {
  const nunjucks = require('nunjucks')
  const config = require('./sonic.js')
  const paths = require('../sonic/paths.js')
  const templateTags = require('../sonic/template-tags')

  const path = `${paths.project.sourcePath}/`
  const ext = '.html'

  const data = {}
  const loaders = []

  const envOptions = {
    autoescape: false,
    throwOnUndefined: false,
    trimBlocks: true,
    lstripBlocks: true,
    watch: false,
    noCache: false,
    useCache: true,
    async: false,
    express: null,
    tags: null
  }

  const manageEnv = function (env) {
    // Set context variables
    env.addGlobal('environment', api.env)

    env.addGlobal('site_name', config.project.longName || '')
    env.addGlobal('site_description', config.project.description || '')
    env.addGlobal('static', paths.project.staticURI)

    env.addFilter('interpolate', function (str) {
      return nunjucks.renderString(str, this.ctx)
    })

    function * entries (obj) {
      for (const key of Object.keys(obj)) {
        yield [key, obj[key]]
      }
    }

    for (const [name, callback] of entries(templateTags)) {
      if (name === 'expand') {
        env.addGlobal(name, (pattern, cwd = paths.project.sourcePath) => callback(pattern, cwd))
      } else {
        env.addGlobal(name, callback)
        env.addFilter(name, callback)
      }
    }
  }

  return { nunjucks: { path, ext, data, manageEnv, loaders }, envOptions }
}
