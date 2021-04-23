
const showVersion = require('./show-version.js')
const showHelp = require('./show-help.js')
const traceRequire = require('./trace-require.js')
const checkNodeModules = require('./check-node-modules.js')
const checkNodeVersion = require('./check-node-version.js')

// CLI arguments
function cliArguments () {
  // Shows version number
  if (process.argv.includes('version') || process.argv.includes('--version') || process.argv.includes('-V')) {
    require('./print-bootlogo.js')(null)
    showVersion()
  }

  // Shows help information
  if (process.argv.includes('help') || process.argv.includes('--help') || process.argv.includes('-H')) {
    require('./print-bootlogo.js')(null)
    showHelp()
  }

  // Allows tracing require calls for optimization purposes.
  if (process.argv.includes('trace-require') || process.argv.includes('--trace-require') || process.argv.includes('-TR')) {
    traceRequire()
  }

  // Allows profiling the cpu usage for optimization purposes.
  if (process.argv.includes('profile-cpu') || process.argv.includes('--profile-cpu') || process.argv.includes('-PC')) {
    const profiler = require('./profiler.js')
    profiler.init({ type: 'cpu' })
    profiler.start()
    process.on('exit', () => profiler.stop())
  }

  // Allows profiling the heap usage for optimizatin purposes.
  if (process.argv.includes('profile-heap') || process.argv.includes('--profile-heap') || process.argv.includes('-PH')) {
    const profiler = require('./profiler.js')
    profiler.init({ type: 'heap' })
    profiler.start()
    process.on('exit', () => profiler.stop())
  }

  // Allows profiling a heap snapsnot for optimization purposes.
  if (process.argv.includes('profile-heap-snapshot') || process.argv.includes('--profile-heap-snapshot') || process.argv.includes('-PHS')) {
    const profiler = require('./profiler.js')
    profiler.init({ type: 'heap-snapshot' })
    profiler.start()
    process.on('exit', () => profiler.stop())
  }

  // Check if packages are installed and runs Yarn if they're not.
  if (!process.argv.includes('skip-node-modules-check') && !process.argv.includes('--skip-node-modules-check') && !process.argv.includes('-SM')) {
    checkNodeModules()
  }

  // Allows checking if the right node version is used
  if (!process.argv.includes('skip-node-version-check') && !process.argv.includes('--skip-node-version-check') && !process.argv.includes('-SV')) {
    checkNodeVersion()
  }

  // Print a nice project image for easy identification
  if (!process.argv.includes('skip-bootlogo') && !process.argv.includes('--skip-bootlogo') && !process.argv.includes('-SB')) {
    require('./print-bootlogo.js')(null)
  }

  // Task list
  if (process.argv.includes('tasks') || process.argv.includes('--tasks') || process.argv.includes('-T') || process.argv.includes('tasks-simple') || process.argv.includes('--tasks-simple') || process.argv.includes('-TS')) {
    if (process.stdout.cursorTo) {
      process.stdout.write('Loading tasks...')
    }

    const tasks = require('../tasks.js')

    if (process.stdout.cursorTo) {
      process.stdout.cursorTo(0)
    }

    Object.keys(tasks).forEach(name => console.log(name, ' '.repeat(20)))
    process.exit(0)
  }
}

module.exports = cliArguments
