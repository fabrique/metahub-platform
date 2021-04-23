// Show about info

function argName (name = '', shortName = '', altName = '', altShortName = '') {
  let result = ` \x1b[1m --${name}\x1b[0m`

  if (shortName) {
    result += `,\x1b[1m -${shortName}\x1b[0m`
  }

  if (altName) {
    result += `,\x1b[1m --${altName}\x1b[0m`
  }

  if (altShortName) {
    result += `,\x1b[1m -${altShortName}\x1b[0m`
  }

  return result
}

function argString (string = '', extraString = '') {
  let result = ` \x1b[1m ${string}\x1b[0m`

  if (extraString) {
    result += `\x1b[2m ${extraString}\x1b[0m`
  }

  return result
}

function argDescription (...lines) {
  return '  \x1b[2m └─ \x1b[0m' + lines.join('\n' + (' '.repeat(6)))
}

function argExample (string = '') {
  return `      example: ${string}`
}

module.exports = function showHelp () {
  console.log('\x1b[1mSonic\x1b[0m is a very fast and flexible build system for static')
  console.log('frontend deliverables. Tasks and workflows are simple to add,')
  console.log('change and remove. There is little configuration involved. It')
  console.log('has (relatively) minimal dependencies. It\'s compatible with')
  console.log('most Gulp plugins. Your mileage may vary.')
  console.log('')
  console.log('You might think: "That\'s impossibru!", but here you go.')
  console.log('')
  console.log('Task-related CLI arguments:')
  console.log(argString('<name>'))
  console.log(argDescription('runs the specified flow/task'))
  console.log(argExample('`node sonic scripts` will run the scripts', 'flow/task.'))
  console.log(argString('<nameA> <nameB> ...'))
  console.log(argDescription('runs the specified flows/tasks in sequence'))
  console.log(argExample('`node sonic stylesheets scripts` will first', 'run the stylesheets, and then the scripts.'))
  console.log(argString('<taskname>+<taskname>'))
  console.log(argDescription('runs the specified flows/tasks in parallel \x1b[1m[NOT IMPLEMENTED]\x1b[0m'))
  console.log('')
  console.log('Additive CLI flags:')
  console.log(argName('skip-bootlogo', 'SB'))
  console.log(argDescription('skips displaying the image on startup. (why?)'))
  console.log(argName('skip-node-modules-check', 'SM'))
  console.log(argDescription('skips the check for a `node_modules` folder.'))
  console.log(argName('skip-node-version-check', 'SV'))
  console.log(argDescription('skips the check for the required Node version.', 'proceed at your own risk.'))
  console.log(argName('verbose', 'BLABLA'))
  console.log(argDescription('shows more verbose output in the console'))
  console.log(argName('trace-require', 'TR'))
  console.log(argDescription('trace require() calls, after running the task(s),', 'for bottleneck identification'))
  console.log(argName('profile-cpu', 'PC'))
  console.log(argDescription('profiles cpu usage and saves the results to disk.', 'open in chrome inspector for waterfall inspection'))
  console.log(argName('profile-heap', 'PH'))
  console.log(argDescription('profiles heap usage and saves the results to disk.', 'open in chrome inspector for memory leak identification'))
  console.log(argName('profile-heap-snapshot', 'PHS'))
  console.log(argDescription('profiles a heap snapshot and saves the results to disk.', 'open in chrome inspector for a detailed look'))
  console.log('')
  console.log('Exclusive CLI flags:')
  console.log(argName('version', 'V'))
  console.log(argDescription('shows version number and exits'))
  console.log(argName('help', 'H'))
  console.log(argDescription('shows this help screen and exits'))
  console.log(argName('tasks', 'T', 'simple-tasks', 'ST'))
  console.log(argDescription('shows a list of available tasks and exits'))
  process.exit(0)
}
