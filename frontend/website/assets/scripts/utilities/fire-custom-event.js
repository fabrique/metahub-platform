
// Fire custom event cross-browser
export default function fireCustomEvent (name = '', detail = {}, bubbles = false, cancelable = false) {
  if (!name) {
    return
  }

  window.dispatchEvent(new CustomEvent(name, { bubbles: bubbles, cancelable: cancelable, detail: detail }))
}
