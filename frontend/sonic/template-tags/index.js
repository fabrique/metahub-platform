// Nunjucks Template Tags
// TODO: Rename functions without underscores, due to linting differences between javascript and python implementations.

const { createHash } = require('crypto')
const { existsSync, statSync, readFileSync } = require('fs')
const { join } = require('path')
const { readdirSync } = require('glob')

// Object iterator
function * entries (obj) {
  for (const key of Object.keys(obj)) {
    yield [key, obj[key]]
  }
}

// Support translatable strings via dummy function
// The underscore function is automatically recognized by Django's translation system.
const fakeTranslate = string => string

// Convert from Base64 to ASCII
const atob = string => Buffer.from(string, 'base64').toString('ascii')

// Convert (ascii? unicode?) to Base64
const btoa = string => Buffer.from(string).toString('base64')

// Shallow clone object
const copy = object => ({ ...object })

// Log on the command line
const debug = (...args) => console.log(...args)

// Enable expanding of globbing patterns - for, for example, component imports
const expand = (pattern = '**/*', cwd = './') => readdirSync(pattern, { cwd: cwd })

// Is number even?
const even = number => number === parseFloat(number) ? !(number % 2) : undefined

// Fill an array with the number form 0 to 19, given a 20
const numberToFilledArray = number => [...Array(parseInt(number, 10)).keys()]

// Get a random hash with optional prefix
const randomHash = (prefix = '') => prefix + Math.random().toString(36).slice(2, -2)

// Get random int between min and max
const randomInt = (min = 0, max = 1) => Math.floor(Math.random() * (max - min + 1) + min)

// Round number
const round = number => Math.round(number)

// Split string
const split = (string, key) => (string || '').toString().split(key)

// Trim string
const trim = string => string.toString().trim()

// Set an object's property
const objectAdd = (object, key, value) => {
  object[key] = value

  return ''
}

// Replace an objects value
const objectReplaceValue = (object, key, value_original, value_replacement) => {
  if (value_original !== null || object[key] === value_original) {
    object[key] = value_replacement
  }

  return ''
}

// Left pad string
const leftPad = (string, length, character) => {
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
const objectDump = obj => {
  let ret = '{'

  for (const [key, value] of entries(obj)) {
    ret += `\n\t${key}: "${value}"`
  }

  ret += '\n}\n'

  return ret
}

// Get object keys
const objectKeys = (obj, sort = false) => {
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
const objectValuesToString = obj => {
  let ret = ''

  for (const [key, value] of entries(obj)) {
    ret += `${value}\n`
  }

  return ret
}

// Get object values
const objectValues = (obj, sort = false) => {
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
const generatePlaceholders = (sizes, ratio = '16:9', retinas = [2/*, 3, 4 */], inverted = false) => {
  // Get widths if not supplied - from ratio, if possible
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

const fileHash = function (filepath = '', algorithm = 'sha256') {
  let data

  filepath = join(process.cwd(), filepath)

  if (!existsSync(filepath)) {
    console.log(`File '${filepath}' doesn't seem to exist. Can't get file hash.`)
    return ''
  }

  const mtime = statSync(filepath).mtime

  if (FILE_HASH_CACHE[filepath] && FILE_HASH_CACHE[filepath].mtime === mtime) {
    return FILE_HASH_CACHE[filepath].hash
  }

  const shasum = createHash(algorithm)
  data = readFileSync(filepath, 'utf-8')

  if (!data) {
    return ''
  }

  data = shasum.update(data, 'utf-8')
  const hash = shasum.digest('base64')

  FILE_HASH_CACHE[filepath] = { hash: hash, mtime: mtime }

  return hash
}

const includeRaw = function (filepath) {
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
  ret = ret.replace(/&/g, '-and-') // Replace & with 'and'
  ret = ret.replace(/[^\w\-]+/g, '') // Remove all non-word characters
  ret = ret.replace(/\-\-+/g, '-') // Replace multiple dashes with a single dash
  ret = ret.replace(/^-+/, '') // Trim - from start of text
  ret = ret.replace(/-+$/, '') // Trim - from end of text

  return ret
}

// Merge objects (shallow)
const merge = (...args) => Object.assign(...args)

// Trim contents
const trimContents = (str, tighten = true) => {
  // str = str.replace(/\r?\n|\r/g, ' ')
  str = tighten ? str.replace(/\s\s+/g, ' ') : str
  return str.trim()
}

// Propagate value through object
const propagateValue = (object = {}, keys = [], defaultValue = '') => {
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
const friendlyTimestamp = (timestamp, locale = 'en-US', options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) => new Date(timestamp).toLocaleDateString(locale, options)

module.exports = {
  _: fakeTranslate,
  atob,
  btoa,
  copy,
  debug,
  expand,
  even,
  number_to_filled_array: numberToFilledArray,
  random_hash: randomHash,
  random_int: randomInt,
  round,
  split,
  trim,
  object_add: objectAdd,
  left_pad: leftPad,
  object_dump: objectDump,
  object_keys: objectKeys,
  object_values_to_string: objectValuesToString,
  object_values: objectValues,
  generate_placeholders: generatePlaceholders,
  file_hash: fileHash,
  include_raw: includeRaw,
  object_replace_value: objectReplaceValue,
  slugify,
  merge,
  trim_contents: trimContents,
  propagate_value: propagateValue,
  friendly_timestamp: friendlyTimestamp
}
