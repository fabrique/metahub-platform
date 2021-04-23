// Check the required node version and warn or quit when there's a mismatch

const { existsSync, readFileSync } = require('fs')
const { join } = require('path')

const nodeVersionFilePath = join(process.cwd(), '.node-version')
const packageJSONFilePath = join(process.cwd(), 'package.json')
const engines = require(packageJSONFilePath).engines

const required = getNodeVersion()
const current = process.version.trim()

function getNodeVersion () {
  let version = ''

  // Get node version from .node-version or from the package.json
  if (existsSync(nodeVersionFilePath)) {
    version = readFileSync(nodeVersionFilePath, 'utf8').trim()
  } if (engines && engines.node) {
    version = engines.node
  }

  return version ? `v${version}` : ''
}

module.exports = function checkNodeVersion (continueOnMismatch = false, continueOnUnknown = true) {
  let message = ''
  let exit = false

  if (!required) {
    message = 'Warning: Could not determine the required Node version.\n'
    exit = !continueOnUnknown
  } else if (current !== required) {
    message = `Error: Node ${required} required; you've got ${current}.\nChange the contents of '.node-version' when changing versions.\n`
    exit = !continueOnMismatch
  } else {
    return true
  }

  console[exit ? 'error' : 'warn'](message)
  !exit || process.exit(1)

  return false
}
