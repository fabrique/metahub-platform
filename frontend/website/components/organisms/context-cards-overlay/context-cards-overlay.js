
import { createFocusTrap } from 'focus-trap'
import throttle from 'lodash/throttle'

import Component from '../../../assets/scripts/modules/component'
import SwiperWrapper from '../../../assets/scripts/modules/swiper-wrapper'

const SWIPER_OPTIONS = {
  breakpointsInverse: true,
  breakpoints: {
    530: { slidesPerView: 1 },
    800: { slidesPerView: 1 },
    1180: { slidesPerView: 1 }
  }
}

let timeout

export default class ContextCardsOVerlay extends Component {
  init () {
    this.overlay = document.querySelector('.context-cards-overlay')
    this.overlayButton = this.overlay.querySelector('.context-cards-overlay__overlay-button')
    this.container = this.element.querySelector('.swiper-container')

    if (this.container) {
      this.liveregion = document.createElement('div')
      this.liveregion.setAttribute('aria-live', 'polite')
      this.liveregion.setAttribute('aria-atomic', 'true')
      this.liveregion.setAttribute('class', 'liveregion visuallyhidden')
      this.container.appendChild(this.liveregion)
      this.liveregion.style.position = 'absolute'
    }

    let swiperOptions = { ...SWIPER_OPTIONS }

    if ([...this.container.querySelectorAll('.swiper-slide')].length < 2) {
      swiperOptions = { ...swiperOptions, ...{ noSwipe: true, navigation: true, pagination: true, loop: true } }
      this.container.querySelectorAll('.swiper-button-prev, .swiper-button-next').forEach(button => button.parentNode.removeChild(button))
    }

    this.swiperWrapper = new SwiperWrapper(this.container, swiperOptions, [], {
      slideChange: () => this.onSwiperSlideChange()
    })

    window.clearTimeout(timeout)
    timeout = window.setTimeout(() => {
      this.onSwiperSlideChange()

      // Warkaround for swiper bug; see https://github.com/nolimits4web/Swiper/issues/2099
      if (SWIPER_OPTIONS.loop) {
        [...this.element.querySelectorAll('.swiper-button-disabled')].forEach(button => {
          button.classList.remove('swiper-button-disabled')
        })
      }
    }, 500)

    this.initAccessibility()
    this.initOverlay()

    window.addEventListener('open-menu', () => this.overlay.classList.add('context-cards-overlay--hide'))
    window.addEventListener('close-menu', () => this.overlay.classList.remove('context-cards-overlay--hide'))
  }

  initOverlay () {
    const throttledToggle = throttle(() => window.requestAnimationFrame(() => this.toggleOverlay()), 350, { leading: true, trailing: true })

    this.overlayButton.addEventListener('click', () => throttledToggle())
  }

  onSwiperSlideChange () {
    this.swiperWrapper.swiper.slidesSizesGrid[1] = this.swiperWrapper.swiper.slidesSizesGrid[1] + 35

    if (!this.swiperWrapper || !this.swiperWrapper.swiper || !this.swiperWrapper.swiper.slides) {
      return
    }

    const current = this.swiperWrapper.swiper.slides[this.swiperWrapper.swiper.activeIndex]
    const all = Object.values(this.swiperWrapper.swiper.slides).filter(slide => !!slide.tagName)
    const currentWithDuplicates = all.filter(slide => slide.getAttribute('data-swiper-slide-index') === current.getAttribute('data-swiper-slide-index'))

    if (this.liveregion) {
      this.liveregion.textContent = `Item ${this.swiperWrapper.swiper.activeIndex + 1} of ${this.swiperWrapper.swiper.slides.length}`
    }

    currentWithDuplicates.forEach(slide => {
      slide.classList.add('swiper-slide--activated')
    })
  }

  toggleOverlay () {
    if (this.overlay.classList.contains('context-cards-overlay--open')) {
      this.overlay.classList.remove('context-cards-overlay--open')
      const scrollY = document.body.style.top
      document.body.style.position = ''
      document.body.style.top = parseInt(scrollY || '0') * -1
    } else {
      this.overlay.classList.add('context-cards-overlay--open')
      document.body.style.top = `-${window.scrollY}px`
      document.body.style.position = 'fixed'
    }
  }

  initAccessibility () {
    this.setAriaHiddenOnOtherElements(false)
    this.hideOverlayTabbableElements(true)

    this.overlayFocusTrap = createFocusTrap(this.overlay, {
      onActivate: () => { },
      onDeactivate: () => {
        this.toggleOverlay(true)
        this.overlayButton.focus()
      },
      escapeDeactivates: true,
      clickOutsideDeactivates: true,
      returnFocusOnDeactivate: false
    })
  }

  setAriaHiddenOnOtherElements (hidden = true) {
    const nonModalDialogVisibleElements = [...document.querySelectorAll('.content')]
    const modalDialogVisibleElements = [...document.querySelectorAll('.context-cards-overlay')]

    nonModalDialogVisibleElements.forEach(element => element.setAttribute('aria-hidden', hidden))
    modalDialogVisibleElements.forEach(element => element.setAttribute('aria-hidden', !hidden))
  }

  hideOverlayTabbableElements (hidden = true) {
    const modalDialogTabbableElements = [...document.querySelectorAll('.context-cards-overlay a[href]')]

    modalDialogTabbableElements.forEach(element => element.classList.toggle('is-hidden', hidden))

    if (hidden) {
      modalDialogTabbableElements.forEach(element => element.setAttribute('tabindex', -1))
    } else {
      modalDialogTabbableElements.forEach(element => element.removeAttribute('tabindex'))
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.context-cards-overlay').forEach(element => {
  element.instance = element.instance || new ContextCardsOVerlay(element)
}))
