
import Component from '../../../assets/scripts/modules/component'

class AnimateSectionComponent extends Component {
  init () {
    window.addEventListener('scrolltrigger-loaded', () => this.initAnimateSection())
  }

  initAnimateSection () {
    console.log('eh')
    const inner = this.element.querySelector('.js-animate-section__inner')
    const outer = this.element.querySelector('.js-animate-section__outer')

    if (!inner || !outer) {
      return
    }

    window.GSAP.set(inner, { scaleY: 0, transformOrigin: '50% 0%' })
    window.GSAP.set(outer, { scaleY: 1, transformOrigin: '50% 100%' })

    this.coming = window.GSAP.timeline({ scrollTrigger: { trigger: this.element, scrub: 0, start: 'top bottom', end: 'top top' }, ease: 'none' })
    this.coming.fromTo(inner, { scaleY: 0, transformOrigin: '50% 0%' }, { scaleY: 1, transformOrigin: '50% 0%', ease: 'none' })

    this.going = window.GSAP.timeline({ scrollTrigger: { trigger: this.element, scrub: 0, start: 'top top', end: 'bottom top' }, ease: 'none' })
    this.going.fromTo(outer, { scaleY: 1, transformOrigin: '50% 100%' }, { scaleY: 0, ease: 'none', transformOrigin: '50% 100%' })

    // window.addEventListener('resize', () => window.requestAnimationFrame(
    //
    // ))
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-animate-section').forEach(element => {
  element.instance = element.instance || new AnimateSectionComponent(element)
}))
