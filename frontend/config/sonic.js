// Sonic configuration

const options = {
  showNotifications: true
}

const project = {
  slug: 'metahub-platform',
  name: 'metahub',
  longName: 'METAhub Platform',
  description: 'Front-end components for METAhub Platform'
}

const server = {
  host: '0.0.0.0',
  port: 8000,
  liveReload: false
}

const staging = {
  user: 'fabrique',
  ip: '83.96.200.4',
  path: '/var/www/metahub-platform/build/',
  url: 'metahub-platform.fabriquehq.nl'
}

const settings = { options, project, server, staging }

try {
  const overrides = require('./sonic.local.js')

  for (const [name, values] of Object.entries(overrides)) {
    settings[name] = { ...settings[name], ...values }
  }
} catch (e) {
  //
} finally {
  module.exports = settings
}
