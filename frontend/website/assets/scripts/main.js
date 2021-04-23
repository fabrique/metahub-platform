
require('../../components/**/*.js')

// There are 4 load events:
// - 'init-immediate': (compiles when the script is loaded; blocks rendering)
// - 'init-load': (on DOMContentLoaded event; does not block rendering)
// - 'init-after-load': (on Load event, slightly after DOMContentLoaded)
// - 'init-delayed-load': (after Load event, with a slight delay, for iframes and such)
// Usually, the 'init-load' event will suffice.
window.dispatchEvent(new CustomEvent('init-immediate'))
window.addEventListener('DOMContentLoaded', () => window.dispatchEvent(new CustomEvent('init-load')))
window.addEventListener('load', () => window.dispatchEvent(new CustomEvent('init-after-load')))
window.addEventListener('load', () => window.setTimeout(() => window.dispatchEvent(new CustomEvent('init-delayed-load')), 500))

// Focus stuff
document.addEventListener('keydown', () => document.documentElement.classList.add('key-pressed'))
document.addEventListener('mousedown', () => document.documentElement.classList.remove('key-pressed'))
document.addEventListener('touchstart', () => document.documentElement.classList.remove('key-pressed'))

// loading="lazy" polyfill (~3kB) - for non-Chrome
if (!('loading' in HTMLImageElement.prototype)) {
  require('loading-attribute-polyfill')
}

// Import smooth scroll (~35kB) - for Safari and Edge
if (!('scrollBehavior' in document.documentElement.style)) {
  const smoothscroll = require('smoothscroll-polyfill')
  smoothscroll.polyfill()
}

if (window.navigator.userAgent.indexOf('Safari') !== -1) {
  // Web animations polyfill ~(50kB) - for Safari and Edge
  // About 50kb raw, so only use if you need it.
  // const x = import('web-animations-js')
}

console.log('\n %cMade with %c♥%c by Fabrique \n', 'font: 16px serif;', 'font: 13px serif; color: #f00;', 'font: 16px serif;')

const resizeHandlerVH = () => {
  const styleRoot = document.documentElement.style
  const width = document.documentElement.clientWidth
  const height = document.documentElement.clientHeight
  styleRoot.setProperty('--real-100vw', `${width}px`)
  styleRoot.setProperty('--real-1vw', `${width / 100}px`)
  styleRoot.setProperty('--real-100vh', `${height}px`)
  styleRoot.setProperty('--real-1vh', `${height / 100}px`)
}
window.addEventListener('resize', () => resizeHandlerVH(), { passive: true })
resizeHandlerVH()
