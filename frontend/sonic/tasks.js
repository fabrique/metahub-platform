
const { series, parallel } = require('./utilities/run-tasks.js')
const config = require('../config/sonic.js')

// Import base tasks
const clean = require('./tasks/clean.js')
const cleanCache = require('./tasks/clean-cache.js')
const fonts = require('./tasks/fonts.js')
const icons = require('./tasks/icons.js')
const images = require('./tasks/images.js')
const media = require('./tasks/media.js')
const scripts = require('./tasks/scripts.js')
const server = require('./tasks/server.js')
const stylesheets = require('./tasks/stylesheets.js')
const sync = require('./tasks/sync.js')
const templates = require('./tasks/templates.js')
const vendor = require('./tasks/vendor.js')

const { basename } = require('path')
const paths = require('../config/sonic.paths.js')
const watch = require('@eklingen/watch-debounced')

// Switch from development to production
const env = callback => {
  global.buildEnv = 'production'
  console.log(`❯   Using \x1b[31m${global.buildEnv}\x1b[0m environment`)
  callback()
}

// Switch to copying files instead of symlinking (for Drupal)
const fullcopy = callback => {
  global.useSymlinks = false
  console.log(`❯   Will \x1b[31mcopy files\x1b[0m instead of symlinking them`)
  callback()
}

// Compose end-user tasks
const links = series(cb => cb(console.log('❯   \x1b[34mProcessing\x1b[0m links...')), parallel(vendor, fonts, images, media))
const lint = series(cb => cb(console.log('❯   \x1b[34mLinting\x1b[0m sources...')), stylesheets.lint, scripts.lint)
const assets = series(cb => cb(console.log('❯   \x1b[34mBuilding\x1b[0m assets...')), icons, scripts, stylesheets, templates)

const buildPackage = series(cleanCache, env, fullcopy, clean, cb => cb(console.log('❯   \x1b[33mStarting build package from scratch!\x1b[0m')), links, lint, assets)
const build = series(cleanCache, env, clean, cb => cb(console.log('❯   \x1b[33mStarting build from scratch!\x1b[0m')), links, lint, assets)
const deploy = series(cleanCache, build, cb => cb(console.log(`❯   \x1b[34mDeploying\x1b[0m to \x1b[36;4mhttps://${config.staging.url}\x1b[0m...`)), sync)
const start = series(cleanCache, lint, links, assets, parallel(server, watchFiles))

// Watch files for changes
// TODO: Refactor glob-watch so that we can run multiple different tasks per source, per event. Add single file linting and such
// TODO: Events can be fired multiple times from fsevents! Debounce em!
function watchFiles (callback) {
  const queues = {}
  const timeouts = {}

  const applyTask = taskName => {
    if (!queues[taskName]) {
      return
    }

    queues[taskName]() // Don't do anything with the result

    queues[taskName] = null
    clearTimeout(timeouts[taskName])
  }

  const watchGlobCallback = (taskName = 'default', waitDelay = 150, event, path, stats, ...callbacks) => {
    const decorations = { change: '\x1b[33;1;m~\x1b[0m', add: '\x1b[32;1;m+\x1b[0m', unlink: '\x1b[31;1;m-\x1b[0m' }
    const timestamp = () => `\x1b[2m${new Date().toISOString().substr(11, 8)}\x1b[0m`

    console.log(timestamp(), decorations[event], basename(path))

    if (stats) {
      console.log(stats)
    }

    queues[taskName] = series(...callbacks)

    if (timeouts[taskName]) {
      clearTimeout(timeouts[taskName])
    }

    timeouts[taskName] = setTimeout(() => applyTask(taskName), waitDelay)
  }

  watch(paths.fonts.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('fonts', 150, event, path, stats, fonts))
  watch(paths.icons.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('icons', 150, event, path, stats, icons))
  watch(paths.images.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('images', 500, event, path, stats, /* images.optimize, */ images))
  watch(paths.media.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('media', 500, event, path, stats, /* media.optimize, */ media))
  watch(paths.scripts.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('scripts', 150, event, path, stats, scripts.lint, scripts))
  watch(paths.stylesheets.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('stylesheets', 150, event, path, stats, stylesheets.lint, stylesheets))
  watch(paths.templates.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('templates', 150, event, path, stats, templates))
  watch(paths.vendor.watchGlobs, { delay: 1000 }, (event, path, stats) => watchGlobCallback('vendor', 150, event, path, stats, vendor))

  global.isWatching = true
  console.log('❯   \x1b[38;2;195;145;255mReady\x1b[0m and \x1b[35mwatching\x1b[0m 👀') // in ${tasks.map(item => item.name).join(', ')}...`)
  global.exitMessage = '❯   Bye! 👋 Miss you long time!'

  return callback()
}

// Basic task exports
module.exports = { env, fullcopy, clean, 'clean-cache': cleanCache, fonts, icons, images, media, scripts, server, stylesheets, sync, templates, vendor }
// Composited task exports
module.exports = { ...module.exports, lint, assets, links, build, package: buildPackage, deploy, start, watch: watchFiles }
// Alias exports
module.exports = { ...module.exports, serve: server, default: start, 'optimize-images': images.optimize, 'optimize-media': media.optimize, 'lint-scripts': scripts.lint, 'lint-stylesheets': stylesheets.lint }
