// Nunjucks Template Tags

const { createHash } = require('crypto')
const { existsSync, statSync, readFileSync } = require('fs')
const { join } = require('path')

// Object iterator
function * entries (obj) {
  for (const key of Object.keys(obj)) {
    yield [key, obj[key]]
  }
}

// Convert from Base64 to ASCII
const atob = string => Buffer.from(string, 'base64').toString('ascii')

// Convert (ascii? unicode?) to Base64
const btoa = string => Buffer.from(string).toString('base64')

// Shallow clone object
const copy = object => ({ ...object })

// Log on the command line
const debug = (...args) => console.log(...args)

// Enable expanding of globbing patterns - for, for example, component imports
const expand = (pattern = '**/*', cwd = './') => glob.readdirSync(pattern, { cwd: cwd })

// Is number even?
const even = number => number === parseFloat(number) ? !(number % 2) : void 0

// Get string length
const length = string => string.toString().length

// Fill an array with the number form 0 to 19, given a 20
const number_to_filled_array = number => [...Array(parseInt(number, 10)).keys()]

// Get a random hash with optional prefix
const random_hash = (prefix = '') => prefix + Math.random().toString(36).slice(2, -2)

// Get random int between min and max
const random_int = (min = 0, max = 1) => Math.floor(Math.random() * (max - min + 1) + min)

// Round number
const round = number => Math.round(number)

// Split string
const split = (string, key) => (string || '').toString().split(key)

// Trim string
const trim = string => string.toString().trim()

// Set an object's property
const object_add = (object, key, value) => {
  object[key] = value

  return ''
}

// Replace an objects value
const object_replace_value = (object, key, value_original, value_replacement) => {
  if (value_original !== null || object[key] === value_original) {
    object[key] = value_replacement
  }

  return ''
}

// Left pad string
const left_pad = (string, length, character) => {
  let i = -1

  string = String(string)
  character = (!character && character !== 0) ? ' ' : character
  length = length - string.length

  while (++i < length) {
    string = character + string
  }

  return string
}

// Object to string
const object_dump = obj => {
  let ret = '{'

  for (const [key, value] of entries(obj)) {
    ret += `\n\t${key}: "${value}"`
  }

  ret += '\n}\n'

  return ret
}

// Get object keys
const object_keys = (obj, sort = false) => {
  const ret = []

  for (const [key, value] of entries(obj)) {
    ret.push(key)
  }

  if (sort) {
    ret.sort()
  }

  return ret
}

// Get object values as string
const object_values_to_string = obj => {
  let ret = ''

  for (const [key, value] of entries(obj)) {
    ret += `${value}\n`
  }

  return ret
}

// Get object values
const object_values = (obj, sort = false) => {
  const ret = []

  for (const [key, value] of entries(obj)) {
    ret.push(value)
  }

  if (sort) {
    ret.sort()
  }

  return ret
}

// Generate placeholder images
// Input: object with sizes for each breakpoint
// Output: Object with image sources for each breakpoint
// We can specify height and width for each 'breakpoint' like so: sizes = { mobile: '640x480', portrait: '800x600' }
// Or, we can only specify heights and a ratio, like so: sizes = { mobile: 640, portrait: 800 }, ratio = '16:9'
// We can also specify the amount of retina values that need to be generated, like so: retinas = [2, 3, 4] for up to 4x
const generate_placeholders = (sizes, ratio = '16:9', retinas = [2/*, 3, 4 */], inverted = false) => {
  // Get widths if not supplied — from ratio, if possible
  for (const [key, value] of entries(sizes)) {
    let size = value.toString().split('x')

    if (size.length === 1) {
      if (ratio) {
        const ratioSplit = ratio.toString().split(':')
        const newHeight = Math.round(value / ratioSplit[0] * ratioSplit[1])

        size = `${value}x${newHeight}`
      } else {
        size = `${value}x${value}`
      }

      sizes[key] = size
    }
  }

  // Add retina sizes
  for (const [key, value] of entries(sizes)) {
    for (const i of retinas) {
      const newKey = `${key}${i}x`
      const splitSize = value.toString().split('x')
      const newWidth = splitSize[0] * i
      const newHeight = splitSize[1] * i

      sizes[newKey] = `${newWidth}x${newHeight}`
    }
  }

  // Add placeholder urls
  for (const [key, value] of entries(sizes)) {
    const splitSize = value.toString().split('x')
    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="${splitSize[0]}" height="${splitSize[1]}" viewBox="0 0 320 240" preserveAspectRatio="xMidYMid slice">
        <rect fill="${inverted ? '#666' : '#170f3d'}" x="-1000%" y="-1000%" width="2100%" height="2100%"/>
        <text fill="${inverted ? '#170f3d' : '#666'}" font-family="Helvetica" font-size="24" text-anchor="middle" alignment-baseline="middle" transform="matrix(1 0 0 1 160 120)">${value.replace('x', '×')}</text>
      </svg>`.replace(/(\n|\s\s)+/g, '')
    const svgBase64 = Buffer.from(svg).toString('base64')

    sizes[key] = `data:image/svg+xml;base64,${svgBase64}`
  }

  return sizes
}

const FILE_HASH_CACHE = {}

const file_hash = function (filepath, algorithm = 'sha256') {
  let shasum
  let data
  let hash

  filepath = join(process.cwd(), filepath)

  if (!existsSync(filepath)) {
    console.log(`File '${filepath}' doesn't seem to exist. Can't get file hash.`)
    return ''
  }

  const mtime = statSync(filepath).mtime

  if (FILE_HASH_CACHE[filepath] && FILE_HASH_CACHE[filepath].mtime === mtime) {
    return FILE_HASH_CACHE[filepath].hash
  }

  shasum = createHash(algorithm)
  data = readFileSync(filepath, 'utf-8')

  if (!data) {
    return ''
  }

  data = shasum.update(data, 'utf-8')
  hash = shasum.digest('base64')

  FILE_HASH_CACHE[filepath] = { hash: hash, mtime: mtime }

  return hash
}

const include_raw = function (filepath) {
  filepath = join(process.cwd(), filepath)

  if (!existsSync(filepath)) {
    console.log(`File '${filepath}' doesn't seem to exist. Can't get file contents.`)
    return ''
  }

  return readFileSync(filepath, 'utf-8') || ''
}

const slugify = function (str = '') {
  const a = 'àáäâãåăæçèéëêǵḧìíïîḿńǹñòóöôœøṕŕßśșțùúüûǘẃẍÿź·/_,:;'
  const b = 'aaaaaaaaceeeeghiiiimnnnooooooprssstuuuuuwxyz------'
  const p = new RegExp(a.split('').join('|'), 'g')

  let ret = str.toString()

  ret = ret.toLowerCase()
  ret = ret.replace(/\s+/g, '-') // Replace spaces with -
  ret = ret.replace(p, c => b.charAt(a.indexOf(c))) // Replace special characters
  ret = ret.replace(/&/g, '-and-') // Replace & with ‘and’
  ret = ret.replace(/[^\w\-]+/g, '') // Remove all non-word characters
  ret = ret.replace(/\-\-+/g, '-') // Replace multiple - with single -
  ret = ret.replace(/^-+/, '') // Trim - from start of text
  ret = ret.replace(/-+$/, '') // Trim - from end of text

  return ret
}

// Merge objects
const merge_objects = (...args) => Object.assign(...args)

// Trim contents
const trim_contents = (str, tighten = true) => {
  // str = str.replace(/\r?\n|\r/g, ' ')
  str = tighten ? str.replace(/\s\s+/g, ' ') : str
  return str.trim()
}

// Propagate value through object
const propagate_value = (object = {}, keys = [], defaultValue = '') => {
  let previousValue

  keys.forEach(key => {
    if (!object[key]) {
      object[key] = previousValue || defaultValue
    }
    previousValue = object[key]
  })

  return object
}

// timestamp to locale date string
const friendly_timestamp = (timestamp, locale = 'en-US', options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) => new Date(timestamp).toLocaleDateString(locale, options)

module.exports = {
  atob,
  btoa,
  copy,
  debug,
  expand,
  even,
  number_to_filled_array,
  random_hash,
  random_int,
  round,
  split,
  trim,
  object_add,
  left_pad,
  object_dump,
  object_keys,
  object_values_to_string,
  object_values,
  generate_placeholders,
  file_hash,
  include_raw,
  object_replace_value,
  slugify,
  merge_objects,
  trim_contents,
  propagate_value,
  friendly_timestamp
}
