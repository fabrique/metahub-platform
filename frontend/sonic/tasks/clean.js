
const { rm } = require('fs')
const paths = require('../../config/sonic.paths.js')

// Clean destination
function clean (callback) {
  return rm(paths.project.destinationPath, { recursive: true, force: true }, callback)
}

module.exports = clean
