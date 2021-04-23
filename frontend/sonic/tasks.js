
const { series, parallel } = require('./utilities/run-tasks.js')
const config = require('../config/sonic.js')

// Import base tasks
const clean = require('./tasks/clean.js')
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
const paths = require('./paths.js')
const watch = require('@eklingen/watch-debounced')

const { utimesSync, closeSync, openSync } = require('fs')
const { resolve } = require('path')

// Switch from development to production
const env = callback => {
  global.buildEnv = 'production'
  console.log(`❯   Using \x1b[31m${global.buildEnv}\x1b[0m environment`)
  callback()
}

// Compose end-user tasks
const links = series(cb => cb(console.log('❯   \x1b[34mProcessing\x1b[0m links...')), parallel(vendor, fonts, images, media))
const lint = series(cb => cb(console.log('❯   \x1b[34mLinting\x1b[0m sources...')), stylesheets.lint, scripts.lint)
const assets = series(cb => cb(console.log('❯   \x1b[34mBuilding\x1b[0m assets...')), icons, scripts, stylesheets, templates)

const build = series(env, clean, cb => cb(console.log('    \x1b[33mStarting from scratch!\x1b[0m')), links, lint, assets)
const deploy = series(build, cb => cb(console.log(`❯   \x1b[34mDeploying\x1b[0m to \x1b[36;4mhttps://${config.staging.url}\x1b[0m...`)), sync)
const start = series(lint, links, assets, parallel(server, watchFiles))

// Trigger python runserver
function triggerPythonRunserver () {
  const filePath = resolve(process.cwd(), './../metahub/', '__init__.py')
  const time = new Date()

  try {
    utimesSync(filePath, time, time)
  } catch (err) {
    closeSync(openSync(filePath, 'w'))
  }
}

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

    const result = queues[taskName]()

    queues[taskName] = null
    clearTimeout(timeouts[taskName])

    if (taskName === 'templates') {
      triggerPythonRunserver()
    }
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
module.exports = { env, clean, fonts, icons, images, media, scripts, server, stylesheets, sync, templates, vendor }
// Composited task exports
module.exports = { ...module.exports, lint, assets, links, build, deploy, start, watch: watchFiles }
// Alias exports
module.exports = { ...module.exports, serve: server, default: start, optimizeImages: images.optimize, optimizeMedia: media.optimize, lintScripts: scripts.lint, lintStylesheets: stylesheets.lint }
