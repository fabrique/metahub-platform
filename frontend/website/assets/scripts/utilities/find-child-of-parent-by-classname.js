
// Find child of parent by classname
export default function findChildOfParentByClassName (element, className) {
  let child = element

  while ((element = element.parentElement) && !element.classList.contains(className)) {
    child = element
  }

  return child
}
