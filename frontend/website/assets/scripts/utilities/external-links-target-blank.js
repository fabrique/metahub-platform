
// Automatically set the target to '_blank' for external links.
export default function setAllExternalLinksToTargetBlank () {
  const elements = document.querySelectorAll('a')

  elements.forEach(element => {
    if (element.href.substr(0, 4) === 'http' && element.href.indexOf(window.location.host) !== -1) {
      if (!element.target) {
        element.target = '_blank'
      }

      element.classList.add('is-external')

      // Prevent TabNabbing; see: https://medium.com/@jitbit/target-blank-the-most-underestimated-vulnerability-ever-96e328301f4c
      element.rel += ' noopener noreferrer'
    }
  })
}
