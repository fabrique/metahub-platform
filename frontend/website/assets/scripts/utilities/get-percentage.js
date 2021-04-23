
import required from './required'

// Somehow, when calculating percentage, negative numbers seem to be forgotten in testing
// Thus, a fumnction that works. See it as the left-pad equiv ;-)

// Calculates a percentage from a start, end and current number.
// Can clamp to a min or max number.
// When hardClamp is set, returns false when outside range, otherwise just the clamped number
// Can also parse to a fixed amount of decimals
export default function getPercentage (start = required(), end = required(), current = required(), clampMin = false, clampMax = false, hardClamp = false, decimals = false) {
  if (start < 0) {
    const offset = -start

    start += offset
    end += offset
    current += offset
  }

  const distance = end - start
  const displacement = current - start

  let percentage = (displacement / distance) * 100

  if (clampMin !== false && percentage < clampMin) {
    percentage = hardClamp ? false : clampMin
  } else if (clampMax !== false && percentage > clampMax) {
    percentage = hardClamp ? false : clampMax
  }

  if (decimals !== false && percentage !== false) {
    percentage = percentage.toFixed(decimals)
  }

  return Number(percentage)
}
