
// Enables synchronous-style sleeping of the main thread
export default function sleep (time = 3000, cb = () => {}, args = {}) {
  let timeout

  return new Promise((resolve) => {
    window.clearTimeout(timeout) // Otherwise it'll eat up your RAM for breakfast
    timeout = window.setTimeout(() => resolve(cb(args)), time)
  })
}
