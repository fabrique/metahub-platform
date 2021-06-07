// Babel configuration

module.exports = (api) => {
  const API_ENV = api.env() // NOT just an empty assignment; Also sets caching!

  const sourceMap = false // Setting this to true breaks sourcemaps
  const comments = true // Setting this to false breaks Webpack chunk names

  const presets = []
  const plugins = []

  presets.push(['@babel/preset-env', {
    debug: false,
    ignoreBrowserslistConfig: true,
    modules: false,
    useBuiltIns: 'usage',
    corejs: 3,
    targets: {
      // TODO: THIS IS A TEST, PRESET-ENV SEEMS TO GET THE WRONG TARGETS FROM THE BROWSERSLIST FILE
      chrome: '84',
      firefox: '79',
      safari: '13.1',
      ios: '13.5',
      // and_chr: 80,
      edge: '84'

      // TODO: Edge in different build! Perhaps pull babel and terser away from webpack!

      /*
      android: "android",
      edge: "edge",
      ie: "ie",
      ie_mob: "ie",
      ios_saf: "ios",
      node: "node",
      op_mob: "opera",
      opera: "opera",
      safari: "safari",
      samsung: "samsung"
      */

      // android: '76'
      // chrome: '76'
      // edge: '17',
      // firefox: '68',
      // ios: '12.3',
      // safari: '12.1'
    }
    // targets: { chrome: 72 }
    // targets: false // { esmodules: true }
  }])

  // To see what's already included in @babel/preset-env, check:
  // http://npm.broofa.com/?q=@babel/preset-env
  // plugins.push('@babel/plugin-...')

  return { presets, plugins, sourceMap, comments }
}
