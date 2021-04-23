
// Tests if passive event listeners are supported.
export default function supportsPassiveListener () {
  let supportsPassive = false

  try {
    window.addEventListener('test', null, Object.defineProperty({}, 'passive', {
      get: function () {
        supportsPassive = true
        return true
      }
    }))
  } catch (e) {
    //
  }

  return supportsPassive
}
