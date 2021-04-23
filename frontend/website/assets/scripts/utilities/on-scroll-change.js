
// This function returns an interval that fires only when the scrollposition has changed
// A simple throttled event listener would bunch up in the queue, causing lag
// A normal interval would cause high cpu usage
// This is the best of both worlds - 60FPS ALL THE THINGS

export default function onScrollChange (cb, ms = 10, scrollElement = window) {
  let interval
  let scrollY = scrollElement.scrollY

  const check = () => {
    if (scrollElement.scrollY === scrollY) {
      return
    }

    scrollY = scrollElement.scrollY

    cb()
  }

  window.clearInterval(interval)
  /* eslint-disable-next-line */
  interval = window.setInterval(check, ms)

  return interval
}
