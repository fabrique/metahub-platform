
// Example plugin wrapper.

// Don't import, but use like so:
// const ScrollTrigger = (await import('../../../assets/scripts/plugins/gsap.scrolltrigger')).default()
// This is so Webpack can automagically split the bundles.

import { ScrollTrigger } from 'gsap/src/ScrollTrigger'

export default function loadGSAP () {
  return ScrollTrigger
}
