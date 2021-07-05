
import Component from '../../../assets/scripts/modules/component'

// Loading GSAP and dumping it into the global window object is... less then ideal.
// But since we're going to use it all over the place... and hey, it works. -EKL
export default class DocumentComponent extends Component {
  async init () {
    await this.loadGSAP()
  }

  async loadGSAP () {
    window.GSAP = window.GSAP || (await import('../../../assets/scripts/plugins/gsap')).default()
    window.ScrollTrigger = window.ScrollTrigger || (await import('../../../assets/scripts/plugins/gsap.scrolltrigger')).default()

    window.GSAP.registerPlugin(window.ScrollTrigger)
    window.GSAP.ticker.sleep() // Prevent GSAP ticker from leaking memory when not in use

    // Check for re-layout and recalculate, otherwise ScrollTrigger can lose track
    const observer = new ResizeObserver(() => window.ScrollTrigger.refresh())
    observer.observe(document.body)

    window.dispatchEvent(new CustomEvent('gsap-loaded'))
    window.dispatchEvent(new CustomEvent('scrolltrigger-loaded'))
  }
}

window.addEventListener('init-immediate', () => {
  document.documentElement.instance = new DocumentComponent(document.documentElement)
})
