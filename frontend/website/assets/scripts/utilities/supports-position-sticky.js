
// Tests if position sticky is supported
export default function supportsPositionSticky () {
  let supportsPositionSticky = false

  const element = document.createElement('div')

  for (const prefix of ['-webkit-', '-ms-', '']) {
    try {
      element.style.position = prefix + 'sticky'
    } catch (e) {
      //
    }

    if (element.style.position !== '') {
      supportsPositionSticky = true
      break
    }
  }

  return supportsPositionSticky
}
