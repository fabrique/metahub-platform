
// Faux decorator for required arguments
export default function required () {
  throw new Error('Missing parameter')
}
