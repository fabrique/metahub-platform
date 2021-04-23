
// Find parent by classname
export default function findParentByClassName (element, className) {
  while ((element = element.parentElement) && !element.classList.contains(className)) {
    //
  }

  return element
}
