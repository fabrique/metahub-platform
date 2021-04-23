
// Find parent by selector
export default function findParentBySelector (element, selector) {
  while ((element = element.parentElement) && !((element.matches || element.matchesSelector).call(element, selector))) {
    //
  }

  return element
}
