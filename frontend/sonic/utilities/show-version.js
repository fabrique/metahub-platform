// Show about info

module.exports = function showVersion () {
  console.log('\x1b[1mSonic\x1b[0m \x1b[2m[codename: PLING PLING PLING]\x1b[0m')
  console.log('Yeah, that\'s about as specific of a version number you\'re gonna get. Sorry \'bout that.')
  process.exit(0)
}
