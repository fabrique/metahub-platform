
// Generate random hash
export default function randomHash () {
  return Math.random().toString(36).slice(2, -2)
}
