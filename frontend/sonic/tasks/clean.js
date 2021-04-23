
const { rmdir } = require('fs')
const paths = require('../paths.js')

// Clean destination
function clean (callback) {
  return rmdir(paths.project.destinationPath, { recursive: true }, callback)
}

module.exports = clean
