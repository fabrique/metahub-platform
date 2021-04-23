// Check if the packages are installed and runs Yarn if tey're not.

module.exports = function checkNodeModules () {
  try {
    require.resolve('vinyl-fs') // Do we have a populated node_modules directory?
  } catch (e) {
    console.warn('🚨  Packages not found! Please run `yarn`.')
    process.exit(1)
  }
}
