
// Fire event cross-browser
export default function fireEvent (element, name = '') {
  if (!element || !name) {
    return
  }

  const evt = document.createEvent('HTMLEvents')
  evt.initEvent(name, false, true)
  element.dispatchEvent(evt)
}
