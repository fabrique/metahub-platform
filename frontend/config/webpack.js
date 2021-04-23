// Webpack configuration

const { join, relative } = require('path')

const basename = (suffix = '', name = '[name].[ext]') => (suffix ? name.replace(/\[name]/i, `[name]-${suffix}`) : name).replace(/\[ext]/i, 'js')
// TODO: Add -[contenthash] after name - but how to load it in templates?

module.exports = env => {
  const webpack = require('webpack')
  const TerserPlugin = require('terser-webpack-plugin') // Not in dev depenencies; installed by Webpack

  const context = process.cwd()

  const mode = env.mode === 'production' ? 'production' : 'development'
  const src = `${env.src}/`
  const dest = '/static/scripts/'

  const devtool = 'source-map'
  const target = 'web'
  const profile = false // Enable this to analyze stats
  const watch = false
  const stats = 'verbose' // 'errors-only'

  // If a package isn't chunked, use this to force it.
  // Add the package name of any large dependencies (50K+ uncompressed) that may be separated into chunks.
  // Either as a string (eg: 'swiper') or an object (eg: { name: 'swiper', alias: 'carouselthing' }).
  // Use import('xxx') instead of require('xxx') to make webpack automatically extract the chunk
  // NOTE: If your javascript isn't executed, try using an explicit async import: const XXX = await import('XXX')
  const FAT_BASTARDS = [
    // 'swiper',
    // 'smoothscroll-polyfill',
    // 'web-animations-js'
    // { name: 'chart.js', alias: 'chart' }
    // 'moment' // dependency of chart.js
    // 'paper',
  ]

  // Add packages that are included as dependencies, but not used. These will not be output in the final build. If the webpack output is somehow not executing, it's a bit bet you've put a dependency here that is needed.
  const externals = [
    // 'moment' // dependency of chart.js. If you use timescales, remove this entry! Make sure it's in FAT_BASTARDS to prevent your main entry point from blowing up.
  ]

  const performance = {
    hints: false,
    maxEntrypointSize: 1024 * 512,
    maxAssetSize: 1024 * 256
  }

  const resolve = {
    extensions: ['.js'],
    modules: [src, 'node_modules'],
    alias: {},
    plugins: []
  }

  const resolveLoader = {
    plugins: []
  }

  const moduleObj = {
    rules: []
  }

  const optimization = {
    minimize: false,
    chunkIds: (mode === 'production') ? 'deterministic' : 'named',
    moduleIds: (mode === 'production') ? 'deterministic' : 'named'
  }

  if (mode === 'production') {
    const terserPluginOptions = {
      cache: true,
      parallel: true,
      sourceMap: true,
      extractComments: false,
      terserOptions: {
        compress: true,
        ie8: false,
        mangle: false,
        safari10: false,
        webkit: false,
        output: {
          beautify: true,
          comments: false,
          ecma: 8,
          indent_level: 2,
          // preamble: '/* Made with ❤️ by Fabrique */\n',
          quote_style: 3,
          semicolons: false,
          wrap_iife: false
        }
      }
    }

    optimization.minimize = true
    optimization.minimizer = [
      new TerserPlugin(terserPluginOptions)
    ]
  }

  const plugins = []

  const output = {
    publicPath: dest,
    ecmaVersion: 2020 // for webpack v5
  }

  const cache = {
    type: 'filesystem',
    buildDependencies: {
      // TODO: Get these urls from sonic config?
      config: [module.filename], // get cache invalidation on config change
      sources: [
        join(process.cwd(), 'website/assets/scripts/'),
        join(process.cwd(), 'website/components/')
      ]
    }
  }

  plugins.push(new webpack.DefinePlugin({
    WEBPACK_ENV: { ENV: `"${env.mode}"` }
  }))

  moduleObj.rules.push({
    enforce: 'pre',
    test: /.*\.js$/,
    exclude: /node_modules/,
    loader: require.resolve(join(process.cwd(), 'sonic/plugins/webpack/glob-loader')),
    options: { test: '(import|require)', delimiter: '\n' }
  })

  optimization.splitChunks = {
    cacheGroups: {
      default: false,
      defaultVendors: false
    }
  }

  for (const entry of FAT_BASTARDS) {
    const name = entry.name ? entry.name : entry
    const alias = entry.alias ? entry.alias : entry

    optimization.splitChunks.cacheGroups[alias] = {
      chunks: chunk => ['main'].includes(chunk.name),
      name: alias, // name.replace('.js', ''),
      test: module => new RegExp(`/node_modules\\/${name}/`).test(module.context),
      reuseExistingChunk: true,
      minChunks: 1,
      minSize: 0
    }
  }

  moduleObj.rules.push({
    test: /.*\.js$/,
    exclude: /node_modules/,
    loader: require.resolve('babel-loader'),
    options: { extends: join(process.cwd(), 'config/babel'), cacheDirectory: true, envName: mode }
  })

  output.filename = basename()
  output.chunkFilename = basename()

  return {
    context,
    mode,
    devtool,
    target,
    profile,
    watch,
    stats,
    externals,
    performance,
    resolve,
    resolveLoader,
    optimization,
    plugins,
    module: moduleObj,
    output,
    cache
  }
}
