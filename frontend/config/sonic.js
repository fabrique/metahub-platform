// Sonic configuration

const options = {
  showNotifications: true
}

const project = {
  slug: 'metahub',
  name: 'MetaHub',
  longName: 'Jüdisches Museum Frankfurt',
  description: 'Static templates for Jüdisches Museum Frankfurt'
}

const server = {
  host: '0.0.0.0',
  port: 8080,
  liveReload: false
}

const staging = {
  user: 'fabrique',
  ip: '83.96.200.4',
  path: '/var/www/metahub/build/',
  url: 'metahub.fabriquehq.nl'
}

const settings = { options, project, server, staging }

try {
  const overrides = require('./sonic.local.js')

  for (const [name, values] of Object.entries(overrides)) {
    settings[name] = { ...settings[name], ...values }
  }
} finally {
  module.exports = settings
}
