
// Get scroll percentage of the document
export default function getScrollPercentage () {
  return (document.documentElement.scrollTop || document.body.scrollTop) / ((document.scrollingElement.scrollHeight || document.body.scrollHeight) - document.documentElement.clientHeight) * 100
}
