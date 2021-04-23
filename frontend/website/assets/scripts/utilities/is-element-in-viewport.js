
// Checks if an element is in the viewport
// Returns the bounding rect if true, false if not
// You can give an extra offset if, for example, tweens will move outside the element's boundary
// This is because transforms and such are on a separate layer and as such, not counted (i think)
export default function isElementInViewport (element, extraOffset = 0) {
  const rect = element.getBoundingClientRect()
  /* eslint-disable-next-line */
  const isInViewport = (rect.top <= (window.innerHeight + extraOffset) && (rect.top + element.offsetHeight + extraOffset) >= 0)

  return isInViewport ? rect : false
}
