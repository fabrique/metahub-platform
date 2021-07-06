export default function TitleTween (element, start = 1, end = 2) {
  if (!element) {
    return
  }

  const initTween = () => {
    // Set tween
    window.GSAP.set(element, { force3D: true }) // We're gonna be needing the GPU real soon
    window.GSAP.fromTo(element, { scaleY: start }, { scaleY: end, scrollTrigger: { trigger: element.parentNode, scrub: 0.15 }, ease: 'linear' })

    const sections = document.querySelectorAll('.js-animate-section')

    sections.forEach(section => {
      const wrapper = section.querySelector('.js-animate-section__inner')
      console.log('wrapper', wrapper)
      console.log('section', section)
      window.GSAP.set(wrapper, { scaleY: 0, transformOrigin: '50% 100%' })

      const tl = window.GSAP.timeline({
        scrollTrigger: {
          trigger: section,
          scrub: true,
          start: 'top bottom',
          end: 'top top'
        },
        ease: 'none'
      })

      tl.fromTo(wrapper, {
        scaleY: 0,
        transformOrigin: '50% 0%'
      }, {
        scaleY: 1,
        transformOrigin: '50% 0%'
      })
    })

    // window.GSAP.set(card, { force3D: true }) // We're gonna be needing the GPU real soon
    // window.GSAP.fromTo(card, { y: start }, { y: end, scrollTrigger: { trigger: cardWrapper, scrub: 0 }, ease: 'linear' })
    // window.ScrollTrigger.create({ trigger: card, start: '100px bottom', onEnter: () => card.classList.add('composition-card--inview') })
  }

  window.addEventListener('scrolltrigger-loaded', () => initTween())
  window.addEventListener('resize', () => window.requestAnimationFrame(() => initTween()))
}
