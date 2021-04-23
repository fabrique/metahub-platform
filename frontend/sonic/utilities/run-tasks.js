
const { map, mapSeries } = require('now-and-later')
const asyncDone = require('async-done')

function series (...callbacks) {
  return done => mapSeries(callbacks, (fn, key, cb) => asyncDone(fn, cb), null, done)
}

function parallel (...callbacks) {
  return done => map(callbacks, (fn, key, cb) => asyncDone(fn, cb), null, done)
}

module.exports = {
  series, parallel
}
