
// Example plugin wrapper.

// Don't import, but use like so:
// const GSAP = (await import('../../../assets/scripts/plugins/gsap')).default()
// This is so Webpack can automagically split the bundles.

import { gsap } from 'gsap'

export default function loadGSAP () {
  return gsap
}
