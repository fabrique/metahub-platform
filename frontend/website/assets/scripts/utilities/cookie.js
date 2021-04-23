// jshint module: true

// Get or set cookies
// Shameless copy paste from the wide webs
export default function cookie (name, value, options) {
  if (arguments.length < 2) {
    return get(name)
  }

  set(name, value, options)
}

function set (name, value, options = {}) {
  let str = `${window.encodeURIComponent(name)}=${window.encodeURIComponent(value)}`

  if (value === null) {
    options.maxage = 356
  }

  if (!options.maxage && !options.expires) {
    options.expires = new Date(new Date().setFullYear(new Date().getFullYear() + 1))
  }

  if (options.expires) {
    options.expires = new Date(options.expires).toUTCString()
  }

  str += (options.path) ? ';path=' + options.path : ''
  str += (options.domain) ? ';domain=' + options.domain : ''
  str += (options.maxage) ? ';maxage=' + options.maxage : ''
  str += (options.expires) ? ';expires=' + options.expires : ''
  str += (options.secure) ? ';secure=true' : ''
  str += ';'

  document.cookie = str
}

function get (name) {
  const cookies = parse(document.cookie)

  return !!name && cookies[name] ? cookies[name] : null
}

function parse (str) {
  const obj = {}
  const pairs = str.split(/ *; */)

  if (!pairs[0]) {
    return obj
  }

  for (let pair of pairs) {
    pair = pair.split('=')
    obj[window.decodeURIComponent(pair[0])] = window.decodeURIComponent(pair[1])
  }

  return obj
}
