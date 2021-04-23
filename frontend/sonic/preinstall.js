
const { readFileSync } = require('fs')
const { join } = require('path')

// Detect if run by NPM and fail
if (process.env.npm_config_user_agent.indexOf('yarn') === -1) {
  console.log(`
    \x1b[1mHi there! 👋\x1b[0m

    This project uses \x1b[4myarn\x1b[0m (\x1b[36;4mhttps://yarnpkg.com\x1b[0m) for package management instead of npm.
    This, together with version pinning, ensures a fully reproducible build, even in the future.
    It's also much faster. And who likes to wait when they can avoid it?

        to install yarn: . . . . . . . . . . . . \x1b[2m$\x1b[0m\x1b[33m brew install yarn \x1b[0m
        to install the project packages: . . . . \x1b[2m$\x1b[0m\x1b[33m yarn \x1b[0m
        to add a new package:. . . . . . . . . . \x1b[2m$\x1b[0m\x1b[33m yarn add <package-name> \x1b[0m
        to remove a package: . . . . . . . . . . \x1b[2m$\x1b[0m\x1b[33m yarn remove <package-name> \x1b[0m
        to upgrade a package:. . . . . . . . . . \x1b[2m$\x1b[0m\x1b[33m yarn upgrade <package-name> \x1b[0m
        to upgrade all packages: . . . . . . . . \x1b[2m$\x1b[0m\x1b[33m yarn upgrade-interactive --latest \x1b[0m
        to audit existing packages:. . . . . . . \x1b[2m$\x1b[0m\x1b[33m yarn audit \x1b[0m

    For more information, see \x1b[36;4mhttps://yarnpkg.com/en/docs/usage\x1b[0m.

    Footnote: yarn is configured to bootstrap the exact version located inside the project.
        to ugrade the included yarn version: . . \x1b[2m$\x1b[0m\x1b[34m yarn policies set-version \x1b[0m

    - Elco 🦄
  `)
  process.exit(1)
}

// Check the required node version and warn or quit when there's a mismatch
const required = `v${readFileSync(join(process.cwd(), '.node-version'), 'utf8').trim()}`
const current = process.version.trim()

if (!required) {
  console.log(`
    Warning: Could not determine the required Node version.
  `)
} else if (current !== required) {
  console.log(`
    This project \x1b[31mrequires node \x1b[1m${required}\x1b[0m; you've got \x1b[33m${current}\x1b[0m. Quite a sad situation.
    Please install the correct Node version, or change the \x1b[34m.node-version\x1b[0m file to suit.
  `)
  process.exit(1)
}
