
# Fabrique Design System

Static templates for Fabrique Design System.

## Table of Contents

* [Installation](#markdown-header-installation)
* [How to start](#markdown-header-how-to-start)
* [Development](#markdown-header-development)
* [Deployment](#markdown-header-deploymemt)
* [Testing](#markdown-header-testing)
* [Scope](#markdown-header-scope)
* [Used technology stack](#markdown-header-used-technology-stack)
* [TODO](#markdown-header-todo)

## Installation

This project uses [yarn](https://yarnpkg.com) for package management. The required version of [node](https://nodejs.org) is specified in the `.node-version` file. Any other node version is unsupported.

    to install the prerequisites:. . . . . . $ brew install nodenv yarn
    to verify and/or install node: . . . . . $ nodenv version || nodenv install
    to install the project packages: . . . . $ yarn

## How to start

This project uses _sonic_, a tiny custom build system that is compatible with [gulp](https://gulpjs.com)-plugins. It's much faster, but just as flexible.

    to build, watch for changes and serve: . $ node sonic
    to deploy to staging:. . . . . . . . . . $ node sonic deploy

There are extra commands available. These can be combined for serial execution.

    to build in production mode only:. . . . $ node sonic build
    to build and serve only: . . . . . . . . $ node sonic build serve
    to compile the stylesheets only: . . . . $ node sonic stylesheets

    for a list of all available tasks: . . . $ node sonic --tasks
    for a list of all available commands:. . $ node sonic --help

> **TIP** - You can substitute `node sonic` with `node .`

### Custom configuration

<!-- markdownlint-disable -->
By default, the files are served at http://127.0.0.1:8000.
<!-- markdownlint-restore -->

To modify settings, duplicate `./config/sonic.local.example.js` to `./config/sonic.local.js`
and change the values as preferred. This file is local to your machine, and will not be committed to _git_.

    to serve on a different host/port: . . . server: { host: '127.0.0.1', port: 9000 }
    to turn on live reload:. . . . . . . . . server: { liveReload: true }
    to turn off notifications: . . . . . . . options: { notifications: false }

## Development

This project contains static frontend designs.

### Folder structure

The most important folders are noted below.

    build  . . . . . . . . . . . . deliverable static designs
    media  . . . . . . . . . . . . media files (uncompressed source files)
    website  . . . . . . . . . . . source files
     └─ assets . . . . . . . . . . static assets
         └─ fonts  . . . . . . . . webfonts
             └─ <font-name>  . . . files for <font-name> (woff, woff2)
         └─ icons. . . . . . . . . icons (for use in templates)
             └─ <set-name> . . . . files for <set-name> (svg)
         └─ images . . . . . . . . images (non-content, such as logo)
             └─ favicons . . . . . favicons (for bookmarks etc)
         └─ media  . . . . . . . . media (content, such a photos or videos, optimized)
         └─ scripts  . . . . . . . scripts
             └─ modules  . . . . . classes that can be extended
             └─ plugins  . . . . . wrapper for plugins
             └─ utilities  . . . . functions that can be imported
         └─ stylesheets  . . . . . stylesheets
             └─ definitions  . . . variables (such as colors, generic style mixins)
                 └─ typography . . reusable typography (such as heading-1 or paragraph)
             └─ fonts  . . . . . . supplied webfonts
             └─ grid . . . . . . . grid settings and mixins
             └─ plugins  . . . . . mixins for use with plugins
             └─ print  . . . . . . print stylesheets
             └─ utilities  . . . . utilities that can be imported
         └─ vendor . . . . . . . . external files (oldschool style)
     └─ components . . . . . . . . reusable, self-contained components
         └─ atoms  . . . . . . . . small pieces (like a button or an image)
         └─ molecules  . . . . . . small piece-combinations (like a button-list, or a card)
         └─ organisms  . . . . . . full-featured components (with layout)
         └─ structures . . . . . . unique components (can exist only once per page)
     └─ templates  . . . . . . . . templates
         └─ pages  . . . . . . . . page templates
             └─ <page-type>  . . . templates of a certain page type (like overview or content)






### Package management

This project uses [yarn](https://yarnpkg.com) for package management. This, together with version pinning, ensures a fully reproducible build, even in the future. A consequence is that any upgrading a package is a manual action.

    to add a new package:. . . . . . . . . . $ yarn add <package-name>
    to remove a package: . . . . . . . . . . $ yarn remove <package-name>

    to upgrade a package:. . . . . . . . . . $ yarn upgrade <package-name>
    to selectively upgrade all packages: . . $ yarn upgrade-interactive --latest

    to audit installed packages: . . . . . . $ yarn audit

For more information, see [yarnpkg.com/usage](https://yarnpkg.com/en/docs/usage).

#### Verifing after _git pull_

When you pull changes via _git_, it's possible the `package.json` has been modified. In that case, stop _sonic_, run _yarn_ again to verify the installed packages are up to date, and restart _sonic_.

    to stop sonic: . . . . . . . . . . . . . press [cmd + c]
    to verify packages:. . . . . . . . . . . $ yarn
    to start sonic back up:. . . . . . . . . $ node sonic

#### Upgrading _yarn_

yarn is configured to bootstrap the exact version located inside the project. This ensures everybody uses this exact same version of _yarn_ for this project.

    to upgrade yarn locally: . . . . . . . . $ yarn policies set-version


..
..
..


TODO: Go more in depth about Atomic Design, BEM, how to add a component, etc.

#### Adding a component

Copy paste a component folder and modify it.

#### Required knowledge

To continue development on this project, knowledge of the following is required:

| name | description
| ---- | -----------
| [Sass](https://sass-lang.com) | SASS stylesheet language (SCSS syntax variant)
| [ES2019](https://flaviocopes.com/ecmascript/) | JavaScript, including modern additions
| [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout) | CSS Grid

#### Manage scripts

To install a dependency, run `yarn add <name>`.
To remove a dependency, run `yarn remove <dev>`.

#### Using scripts

How you import the scripts depends on how they're built. Modern ES6 modules will work fine with `import (<name>)`. Older scripts (AMD) might need a `require(<name>)`. You can `require()` an ES6 import script by using `require().default`.

To use vendor scripts from other sources, place the script in /website/scripts/vendor/<scriptname>/<scriptname>.js.
Make sure the script is *not* minified, and does *not* have `.min.js` as extension.

TODO: Explain about FAT_BASTARDS, ES6 modules, webpack chunk naming, etc.

#### Icons

See `assets/icons` for svg files.

#### Staging location

The staging location is at http://design-system:fabrique@design-system.fabriquehq.nl.

## Scope

### Project scope

The project scope is: TODO: ADD.

### Browser scope

The browser scope is: TODO: ADD.
GEEN INTERNET EXPLODER

### Device scope

The device scope is: TODO: ADD.

## Used technology stack

This toolchain contains technologies make the life of the developer easier and increase the flexibility for designers.

| name | function | description
| ---- | -------- | -----------
| [Node.JS](https://npmjs.com) | JavaScript runtime | Used to run the included utilities and scripts
| [Yarn](https://yarnpkg.com) | Package manager | Used to (un-)install Node.JS packages in a deterministic manner
| [Sass](https://sass-lang.com) | Stylesheet pre-compiler | Used to compile well-structure SCSS modules into CSS
| [PostCSS](https://github.com/postcss/postcss) | CSS post-processor | Used for CSS output processing
| [Autoprefixer](https://github.com/postcss/autoprefixer) | PostCSS plugin | Used to automatically insert vendor-prefixed properties where needed
| [Babel](https://babeljs.io) | JavaScript pre-compiler | Used to compile and combile well-structured JS modules into deployable assets
| [Babel-Preset-Env](https://babeljs.io/docs/en/next/babel-preset-env.html) | Babel preset | Used to compile modern ES2018 JavaScript into ES5 which is understood by older browsers
| [Webpack](https://webpack.js.org) | Asset bundler | Used to combine multiple CSS and JS sources into single files. Also created minified variant & debug mapping files
| [Nunjucks](https://mozilla.github.io/nunjucks/) | Template engine | Used to parse and compile modular templates for frontend delivery, while keeping logic and requirements human readable
| [Browserslist](https://github.com/browserslist/browserslist) | Browserscope configuration | Used by tools like Babel and Autoprefixer to determine the needed transforms for the given browserscope
| [Editorconfig](https://editorconfig.org) | Editor configuration | Used by editors to auto-configure style rules, like indenting
| [ESLint](https://eslint.org) | JavaScript linter | Used to lint JavaScript source files according to certain style rules before the GIT commit
| [Stylelint](https://stylelint.io) | Sass Linter | Used to lint Sass source files according to certain style rules before the GIT commit
| [ImageMin](https://github.com/imagemin/imagemin) | Image compressor | Used to clean & compress images for static frontend testing and delivery
| [Connect](https://github.com/senchalabs/connect) | Simple websever | Used to serve static pages for development

## TODO

See [TODO.md](./TODO.md).
