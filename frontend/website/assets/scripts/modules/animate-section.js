
export default function AnimateSection (element) {
  if (!element) {
    return
  }

  const initAnimateSection = () => {
    const sections = document.querySelectorAll('.js-animate-section')

    sections.forEach(section => {
      const inner = section.querySelector('.js-animate-section__inner')
      const outer = section.querySelector('.js-animate-section__outer')

      if (!inner || !outer) {
        return
      }

      window.GSAP.set(inner, { scaleY: 0, transformOrigin: '50% 0%' })
      window.GSAP.set(outer, { scaleY: 1, transformOrigin: '50% 100%' })

      const coming = window.GSAP.timeline({ scrollTrigger: { trigger: section, scrub: 0, start: 'top bottom', end: 'top top' }, ease: 'none' })
      coming.fromTo(inner, { scaleY: 0, transformOrigin: '50% 0%' }, { scaleY: 1, transformOrigin: '50% 0%', ease: 'none' })

      const going = window.GSAP.timeline({ scrollTrigger: { trigger: section, scrub: 0, start: 'top top', end: 'bottom top' }, ease: 'none' })
      going.fromTo(outer, { scaleY: 1, transformOrigin: '50% 100%' }, { scaleY: 0, ease: 'none', transformOrigin: '50% 100%' })
    })
  }

  window.addEventListener('scrolltrigger-loaded', () => initAnimateSection())
  window.addEventListener('resize', () => window.requestAnimationFrame(() => initAnimateSection()))
}
