
// This function returns an interval that fires only when certain properties have changed from their previous value. Sort of like an observer, but not.
// This is useful when, for example, changing thing on scroll. It allows you to not have a scroll handler.
// A simple throttled event listener would bunch up in the queue, causing lag. A normal interval would cause high cpu usage.
// This is the best of both worlds - 60FPS ALL THE THINGS
// cb = callback, ms = interval delay in ms, items = an object with an element and a property, eq { element: window, property: 'scrollY' }
let interval

export default function onValuesChange (cb, ms = 10, ...items) {
  const values = {}

  for (const item of items) {
    // We need something to identify the value with, either a name, or a combination of element/property names
    if (!item.name && (!item.element || !item.property)) {
      continue
    }

    item.name = item.name || `${item.element}.${item.property}`

    // If we need to execute a callback to get the property, do it. otherwise look up the property on the object.
    const value = item.cb ? item.cb() : item.element[item.property]

    values[item.name] = value
  }

  function check () {
    let unchanged = true

    for (const item of items) {
      const value = item.cb ? item.cb() : item.element[item.property]

      if (values[item.name] !== value) {
        unchanged = false
        values[item.name] = value
      }
    }

    if (unchanged) {
      return
    }

    cb(values)
  }

  window.clearInterval(interval)
  /* eslint-disable-next-line */
  interval = window.setInterval(check, ms)

  return interval
}
