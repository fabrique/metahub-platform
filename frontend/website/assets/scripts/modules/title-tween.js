export default function TitleTween ({
  element,
  wrapper,
  start = 1,
  end = 2,
  startTrigger = '',
  endTrigger = ''
}) {
  if (!element) {
    return
  }

  const initTween = () => {
    // Set tween
    window.GSAP.set(element, { force3D: true }) // We're gonna be needing the GPU real soon
    window.GSAP.fromTo(
      element,
      {
        scaleY: start,
        transformOrigin: 'bottom center'
      },
      {
        scaleY: end,
        transformOrigin: 'bottom center',
        scrollTrigger: {
          end: endTrigger,
          start: startTrigger,
          trigger: wrapper,
          scrub: 0
        },
        ease: 'linear'
      }
    )

    // window.GSAP.set(card, { force3D: true }) // We're gonna be needing the GPU real soon
    // window.GSAP.fromTo(card, { y: start }, { y: end, scrollTrigger: { trigger: cardWrapper, scrub: 0 }, ease: 'linear' })
    // window.ScrollTrigger.create({ trigger: card, start: '100px bottom', onEnter: () => card.classList.add('composition-card--inview') })
  }

  window.addEventListener('scrolltrigger-loaded', () => initTween())
  window.addEventListener('resize', () => window.requestAnimationFrame(() => initTween()))
}
