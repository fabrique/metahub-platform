
// **Sonic** is a very fast and flexible build system for static frontend deliverables. Tasks and workflows are
// simple to add, change and remove. There is little configuration involved. It has (relatively) minimal dependencies.
// It's compatible with most _Gulp_ plugins. Your mileage may vary.

require('./utilities/cli-arguments.js')() // Check CLI arguments

const config = require('../config/sonic.js')

const timestamp = new Date()
const time = timestamp.toISOString().substr(11, 8)
const welcome = `❯   \x1b[34mStarting \x1b[38;2;255;195;0m${config.project.longName || 'Sonic'}\x1b[0m 🚀 \x1b[2m(${time})\x1b[0m`

console.log(welcome) // Early, because the feeling of snappyness is sometimes more important then actual speed

const { series } = require('./utilities/run-tasks.js')
const tasks = require('./tasks.js')

// Set some globals
global.exitOnError = false
global.isWatching = false
global.useSymlinks = true
global.buildEnv = 'development'
global.showNotifications = config.options.showNotifications
global.verboseOutput = process.argv.includes('--verbose')
global.exitMessage = '❯   Done! ✨ \x1b[2m({time}ms)\x1b[0m'

// Prepare a nice exit message
process.on('exit', () => {
  if (process.stdout.cursorTo) {
    process.stdout.cursorTo(0)
  }

  console.log(global.exitMessage.replace('{time}', new Date() - timestamp))
})

// Running specified tasks from the command line
let args = [...process.argv].filter(arg => arg[0] !== '-' && arg[0] !== '/')

if (args.length) {
  const originalArgs = args
  const wrongArgs = args.filter(name => !tasks[name])
  const rightArgs = args.filter(name => tasks[name])

  // Can't find one of the specified tasks; give a helpful suggestion
  if (rightArgs.length !== originalArgs.length) {
    global.exitMessage = `❯   I did't recognize (one of) the tasks specified: \x1b[34m${wrongArgs.join('\x1b[0m, \x1b[34m')}\x1b[0m. Please try again.`
    process.exit(0)
  }
}

// Reference tasks
args = args.filter(name => tasks[name]).map(name => tasks[name])
// Set the default task if none is given
args = args.length ? args : [tasks.start]
// Running the specified task(s)

const running = series(...args)
running(error => {
  if (error) {
    console.log('Error in Sonic task:', error)
  }
})
