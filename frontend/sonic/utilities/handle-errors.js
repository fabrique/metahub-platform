
const { join } = require('path')
const notifier = require('@eklingen/vinyl-stream-notifier')
const notify = notifier({ icon: join(process.cwd(), '/sonic/images/icon.png') }, () => {})
const through2 = require('through2')

function handleErrors (error) {
  if (!error) {
    return
  }

  if (error.toString().indexOf('\n    at ') === -1 && error.stack) {
    error = `${error.toString()}\n${error.stack.split('\n')[1]}`
  } else {
    error = error.toString().split('\n    at ')[0]
  }

  if (error.toString().indexOf('Error: Error:') !== -1) {
    error = error.replace('Error: Error:', 'Error:') // Temporary workaround
  }

  if (!global.isWatching) {
    console.log(error)
    global.exitMessage = `😡  Can't continue, fix the error first.`
    process.exit(1)
  }

  if (global.showNotifications && global.isWatching) {
    notify({ message: error })
  } else {
    console.log(error)
  }
}

// The patching prevents the need for `.on('error', error => errorHandler(error))` after every single pipe.
// Based on gulp-plumber: https://github.com/floatdrop/gulp-plumber/blob/master/index.js

function patch (stream) {
  if (!stream.pipe2) {
    return
  }

  stream._pipe = stream._pipe || stream.pipe
  stream.pipe = stream.pipe2

  const oldListeners = stream.listeners('error')

  if (oldListeners.length !== 1 || oldListeners[0].name !== 'onerror') {
    return
  }

  stream.removeListener('error', oldListeners[0])

  function onerror2 (error) {
    stream.removeListener('error', onerror2)
    oldListeners[0].call(stream, error)
  }

  stream.on('error', onerror2)
}

function pipe2 (stream) {
  if (!stream) {
    throw new Error('Cannot pipe to undefined.')
  }

  this._pipe.apply(this, arguments)
  this.listeners('error').forEach(item => item.name !== 'onerror' || this.removeListener('error', item))

  if (stream._patched) {
    return stream
  }

  stream.pipe2 = pipe2
  patch(stream)

  if (this.errorHandler) {
    stream.errorHandler = this.errorHandler
    stream.on('error', this.errorHandler.bind(stream))
  }

  return stream
}

function patchPipe (errorHandler = error => handleErrors(error)) {
  const stream = through2.obj()

  stream._patched = true
  stream.errorHandler = errorHandler
  stream.pipe2 = pipe2
  patch(stream)

  return stream
}

module.exports = { handleErrors, patchPipe }
