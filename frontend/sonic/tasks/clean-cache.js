
const { rm } = require('fs')

// Clean cache folders (webpack et al)
function cleanCache (callback) {
  rm('node_modules/.cache/', { recursive: true, force: true }, callback)
}

module.exports = cleanCache
