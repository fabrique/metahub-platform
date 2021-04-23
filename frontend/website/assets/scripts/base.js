
const ua = window.navigator.userAgent
const cl = document.documentElement.classList

// Enable JS className
cl.add('has-js')

// Enable hover(), focus() and hover-and-focus() mixins
cl.add(('ontouchstart' in window) ? 'touch' : 'no-touch')

// Enable iOS classnames (is-ipad, is-iphone, is-ios)
if (ua.indexOf('iPad') !== -1) {
  cl.add('is-ipad')
  cl.add('is-ios')
} else if (ua.indexOf('iPhone') !== -1) {
  cl.add('is-iphone')
  cl.add('is-ios')
}

// Enable OS classnames (is-osx, is-windows)
if (ua.indexOf('Mac OS X') !== -1) {
  cl.add('is-osx')
} else if (ua.indexOf('Windows') !== -1) {
  cl.add('is-windows')
} else if (ua.indexOf('Android') !== -1) {
  cl.add('is-android')
}

// Enable Browser classnames
if (ua.indexOf('Edge/') !== -1) {
  cl.add('is-edge')
} else if (ua.indexOf('Chrome/') !== -1) {
  cl.add('is-chrome')
} else if (ua.indexOf('Firefox/') !== -1) {
  cl.add('is-firefox')
} else if (ua.indexOf('Safari/') !== -1) {
  cl.add('is-safari')
} else if (ua.indexOf('Trident/') !== -1) {
  cl.add('is-ie')
}
