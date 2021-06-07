// Nunjucks configuration

module.exports = function (api) {
  const nunjucks = require('nunjucks')
  const config = require('./sonic.js')
  const paths = require('./sonic.paths.js')
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

  function ExampleCustomBlockTag (env) {
    this.tags = ['customtag']

    this.parse = function (parser, nodes, lexer) {
      const tok = parser.nextToken()
      const args = parser.parseSignature(null, true)

      parser.advanceAfterBlockEnd(tok.value)

      return new nodes.CallExtension(this, 'run', args)
    }

    this.run = function (context, args) {
      return '<span>This is a custom tag</span>'
    }
  }

  const manageEnv = function (env) {
    // Set context variables
    env.addGlobal('environment', api.env)

    env.addGlobal('site_name', config.project.longName || '')
    env.addGlobal('site_description', config.project.description || '')
    env.addGlobal('static', paths.project.staticURI)

    // Set test filter
    env.addFilter('interpolate', function (str) {
      return nunjucks.renderString(str, this.ctx)
    })

    // Add block tags
    env.addExtension('ExampleCustomBlockTag', new ExampleCustomBlockTag(env))

    // Set globals and filters
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
