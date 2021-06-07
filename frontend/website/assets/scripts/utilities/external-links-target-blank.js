
// Automatically set the target to '_blank' for external links.
export default function setAllExternalLinksToTargetBlank (exceptionStrings = []) {
  const elements = document.querySelectorAll('a')

  elements.forEach(element => {
    let isLocal = false

    // Same host, so local
    if (element.href.indexOf(window.location.host) !== -1) {
      isLocal = true
    }

    // Starts with / (and not //), so local
    if (element.href.substr(0, 1) === '/' && element.href.substr(1, 1) !== '/') {
      isLocal = true
    }

    // Doesn't start with `http`(s) or `//`, so local
    if (element.href.substr(0, 4) !== 'http' && element.href.substr(0, 2) !== '//') {
      isLocal = true
    }

    for (const exceptionString of exceptionStrings) {
      // Exception found, so treat as local
      if (element.href.indexOf(exceptionString) !== -1) {
        isLocal = true
      }
    }

    if (!isLocal && element.target.indexOf('_blank') === -1) {
      const target = element.target.split(' ')
      target.push('_blank')
      element.target = target.join(' ')
    }

    element.classList.toggle('is-external', !isLocal)
    element.classList.toggle('is-internal', isLocal)

    if (!isLocal) {
      // Prevent TabNabbing; see: https://medium.com/@jitbit/target-blank-the-most-underestimated-vulnerability-ever-96e328301f4c
      element.rel += ' noopener noreferrer'
    }
  })
}
