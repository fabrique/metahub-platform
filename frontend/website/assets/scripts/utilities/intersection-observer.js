
import IntersectionObserver from 'intersection-observer-polyfill/dist/IntersectionObserver'

// Simple IntersectionObserver wrapper; allows fine-grained control options by generating a list of thresholds,
// and easier live debugging of intersections.

function generateMultipleThresholds (count = 10) {
  const thresholds = [...Array(count)].map((v, i) => i / count) // Array: 0 ... 0.25 ... 0.50 ... 0.75 ... 1

  // Thresholds *must* be between 0 and 1. So put the outermost points as far as possible.
  thresholds[0] = 0.001
  thresholds[thresholds.length - 1] = 0.999

  return thresholds
}

function getOrCreateDebugElement () {
  let element = document.getElementById('intersection-observer-debug-tooltip')

  if (element) {
    return element
  }

  element = document.createElement('div')
  element.id = 'intersection-observer-debug-tooltip'

  element.style.background = '#000'
  element.style.color = '#fff'
  element.style.display = 'inline-block'
  element.style.fontSize = '12px'
  element.style.left = 0
  element.style.lineHeight = '8px'
  element.style.opacity = 0.65
  element.style.padding = '12px 15px'
  element.style.position = 'fixed'
  element.style.top = 0
  element.style.whitespace = 'pre'
  element.style.zIndex = '9000'

  document.body.appendChild(element)

  return element
}

function printDebugInfo (change) {
  const element = getOrCreateDebugElement()

  const string = `
    boundingClientRect:\n
      \ttop: ${change.boundingClientRect.top}\n
      \tright: ${change.boundingClientRect.right}\n
      \tbottom: ${change.boundingClientRect.bottom}\n
      \tleft: ${change.boundingClientRect.left}\n
      \twidth: ${change.boundingClientRect.width}\n
      \theight: ${change.boundingClientRect.height}\n
    intersectionRatio: ${change.intersectionRatio.toFixed(3)}\n
    intersectionRect:\n
      \ttop: ${change.intersectionRect.top}\n
      \tright: ${change.intersectionRect.right}\n
      \tbottom: ${change.intersectionRect.bottom}\n
      \tleft: ${change.intersectionRect.left}\n
      \twidth: ${change.intersectionRect.width}\n
      \theight: ${change.intersectionRect.height}\n
    rootBounds:\n
      \ttop: ${change.rootBounds.top}\n
      \tright: ${change.rootBounds.right}\n
      \tbottom: ${change.rootBounds.bottom}\n
      \tleft: ${change.rootBounds.left}\n
      \twidth: ${change.rootBounds.width}\n
      \theight: ${change.rootBounds.height}\n
    target: (element)\n
    time: ${change.time.toFixed(2)}\n
  `

  element.innerText = string
}

// @param handler: function (passed to IntersectionObserver)
// @param options: object (passed to IntersectionObserver)
// @param thresholdCount: boolean or number (if specified, options.threshold will be overwritten)
// @param measureCenter: boolean (if false, then it measures the viewport edges like default, if true it measures the offset from the center of the viewport)
//   NOTE: even if true, you can still influence the offset by using the IntersectionObserver rootMargin option.
//   The element option is then ignored when given.
// @param stopWatchenWhenVisible: boolean
// @param debug: boolean
// @returns the IntersectionObserver instance
export default function InteractionObserverWrapper (handler = () => {}, options = {}, thresholdCount = false, stopWatchingWhenVisible = false, debug = false) {
  if (thresholdCount) {
    options.threshold = generateMultipleThresholds(thresholdCount)
  }

  const observer = new IntersectionObserver(observationHandler, options)

  function observationHandler (changes) {
    for (const change of changes) {
      const element = change.target

      if (debug) {
        printDebugInfo(change)
      }

      handler(change)

      if (stopWatchingWhenVisible) {
        observationHandler(observer.takeRecords())
        observer.unobserve(element)
      }
    }
  }

  return observer
}
