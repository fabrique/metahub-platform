
import focusTrap from 'focus-trap'
import throttle from 'lodash/throttle'
import panzoom from 'panzoom'

import Component from '../../../assets/scripts/modules/component'
import SwiperWrapper from '../../../assets/scripts/modules/swiper-wrapper'

const SWIPER_OPTIONS = {
  // spaceBetween: 16,
  // loop: true,
  // loopAdditionalSlides: 4
  breakpointsInverse: true,
  breakpoints: {
    530: { slidesPerView: 1 },
    800: { slidesPerView: 1 },
    1180: { slidesPerView: 1 }
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev'
  },
  noSwipe: true,
  allowTouchMove: false,
  grabCursor: false
}

// Separate because they are also used elsewhere
const MIN_ZOOM = 0.25
const MAX_ZOOM = 5
const INITIAL_ZOOM = 1

const PANZOOM_OPTIONS = {
  minZoom: MIN_ZOOM,
  maxZoom: MAX_ZOOM,
  initialZoom: INITIAL_ZOOM,
  zoomDoubleClickSpeed: 2, // Disable double click zoom
  bounds: true,
  boundsPadding: 0.25
  // zoomSpeed: 0.065,
}

let timeout

export default class Lightbox extends Component {
  init () {
    this.overlayPhotos = document.querySelector('.lightbox--photo-series')
    this.overlayObjects = document.querySelector('.lightbox--object-series')

    this.buttonClose = this.element.querySelector('.lightbox__button-close')
    this.zoomInButton = this.element.querySelector('.lightbox__button-zoom-in')
    this.zoomOutButton = this.element.querySelector('.lightbox__button-zoom-out')
    this.informationButtons = [...this.element.querySelectorAll('.lightbox__information-title')]
    this.informationContainer = this.element.querySelector('.lightbox__information-container')
    this.panzoomContainers = [...this.element.querySelectorAll('.panzoom-container')]

    this.observer = null
    this.container = this.element.querySelector('.swiper-container')

    this.initAccessibility()
    this.initOverlay()

    if (this.container) {
      this.liveregion = document.createElement('div')
      this.liveregion.setAttribute('aria-live', 'polite')
      this.liveregion.setAttribute('aria-atomic', 'true')
      this.liveregion.setAttribute('class', 'liveregion visuallyhidden')
      this.element.appendChild(this.liveregion)
      this.liveregion.style.position = 'absolute'
      this.liveregion.style.opacity = '0'

      let swiperOptions = { ...SWIPER_OPTIONS }

      if ([...this.container.querySelectorAll('.swiper-slide')].length < 2) {
        swiperOptions = { ...swiperOptions, ...{ navigation: true, pagination: true, loop: true, touchRatio: 0, onlyExternal: true } }
        this.container.querySelectorAll('.swiper-button-prev, .swiper-button-next').forEach(button => button.parentNode.removeChild(button))
      }

      this.swiperWrapper = new SwiperWrapper(this.container, swiperOptions, [], {
        slideChange: () => this.onSwiperSlideChange(),
        slideChangeTransitionEnd: () => this.onSwiperChangeTransitionEnd()
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

      window.addEventListener('detail-slider-updated', (event) => {
        this.swiperWrapper.swiper.slideTo(event.detail)
      })
      window.addEventListener('header-slider-updated', (event) => {
        this.swiperWrapper.swiper.slideTo(event.detail)
      })

      this.panzoomContainers.forEach(container => {
        container.instance = panzoom(container, PANZOOM_OPTIONS)

        console.log(container.instance.getTransform())
        console.log(container.instance)

        const picture = container.querySelector('.picture')

        if (picture) {
          picture.addEventListener('dblclick', event => {
            event.preventDefault()
            event.stopPropagation()

            // somehow, moving and panning at the same time to the center seems to be a large issue with panzoom
            container.instance.setMinZoom(INITIAL_ZOOM)
            container.instance.setMaxZoom(INITIAL_ZOOM)
            container.instance.setTransformOrigin(null)
            container.instance.zoomTo(0, 0, INITIAL_ZOOM)
            container.instance.setMinZoom(MIN_ZOOM)
            container.instance.setMaxZoom(MAX_ZOOM)
            window.requestAnimationFrame(() => container.instance.moveTo(0, 0))
          })
        }
      })
    }
  }

  initOverlay () {
    const throttledToggle = throttle(() => window.requestAnimationFrame(() => this.toggleOverlay()), 350, { leading: true, trailing: true })
    // const throttledToggleObjects = throttle(() => window.requestAnimationFrame(() => this.toggleOverlayObjects()), 350, { leading: true, trailing: true })
    const throttledInfoToggle = throttle(() => window.requestAnimationFrame(() => this.toggleInfoBox()), 350, { leading: true, trailing: true })

    if (this.buttonClose) {
      this.buttonClose.addEventListener('click', () => throttledToggle())
    }

    this.informationButtons.forEach(button => button.addEventListener('click', () => throttledInfoToggle()))

    if (this.zoomInButton && this.zoomOutButton) {
      this.zoomInButton.addEventListener('click', () => this.zoomIn())
      this.zoomOutButton.addEventListener('click', () => this.zoomOut())
    }

    window.addEventListener('open-lightbox', () => throttledToggle())
    // window.addEventListener('open-lightbox--objects', () => throttledToggleObjects())
  }

  toggleOverlay (forceClose = false) {
    // this.overlayObjects.style.display = 'none'
    // this.overlayPhotos.style.display = 'block'

    const closing = forceClose || document.documentElement.classList.contains('overlay-visible')

    if (document.documentElement.classList.contains('overlay-closing') || document.documentElement.classList.contains('overlay-opening')) {
      return
    }

    document.documentElement.classList.toggle('overlay-visible', !closing)
    document.documentElement.classList.toggle('prevent-scrolling', !closing)

    if (!closing) {
      this.setAriaHiddenOnOtherElements(true)
      this.hideOverlayTabbableElements(false)
      this.overlayFocusTrap.activate()
    } else {
      this.overlayFocusTrap.deactivate()
    }

    if (closing) {
      document.documentElement.classList.add('overlay-closing')
      window.setTimeout(() => {
        document.documentElement.classList.remove('overlay-closing')
        this.setAriaHiddenOnOtherElements(false)
        this.hideOverlayTabbableElements(true)
      }, 350)
    } else {
      document.documentElement.classList.add('overlay-opening')
      window.setTimeout(() => {
        document.documentElement.classList.remove('overlay-opening')
      })
    }
  }

  toggleOverlayObjects (forceClose = false) {
    if (this.overlayObjects) {
      this.overlayObjects.style.display = 'block'
    }

    if (this.overlayPhotos) {
      this.overlayPhotos.style.display = 'none'
    }

    const closing = forceClose || document.documentElement.classList.contains('overlay-visible')

    if (document.documentElement.classList.contains('overlay-closing') || document.documentElement.classList.contains('overlay-opening')) {
      return
    }

    document.documentElement.classList.toggle('overlay-visible', !closing)
    document.documentElement.classList.toggle('prevent-scrolling', !closing)

    if (!closing) {
      this.setAriaHiddenOnOtherElements(true)
      this.hideOverlayTabbableElements(false)
      this.overlayFocusTrap.activate()
    } else {
      this.overlayFocusTrap.deactivate()
    }

    if (closing) {
      document.documentElement.classList.add('overlay-closing')
      window.setTimeout(() => {
        document.documentElement.classList.remove('overlay-closing')
        this.setAriaHiddenOnOtherElements(false)
        this.hideOverlayTabbableElements(true)
      }, 350)
    } else {
      document.documentElement.classList.add('overlay-opening')
      window.setTimeout(() => {
        document.documentElement.classList.remove('overlay-opening')
      })
    }
  }

  toggleInfoBox () {
    if (!this.informationContainer) {
      return
    }

    if (this.informationContainer.classList.contains('lightbox__information-container--open')) {
      this.informationContainer.classList.remove('lightbox__information-container--open')
    } else {
      this.informationContainer.classList.add('lightbox__information-container--open')
    }
  }

  zoomIn () {
    const activeSlide = this.element.querySelector('.swiper-slide-active')

    if (!activeSlide) {
      return
    }

    const panzoomContainer = activeSlide.querySelector('.panzoom-container')

    if (!panzoomContainer) {
      return
    }

    const currentScale = panzoomContainer.instance.getTransform().scale || 1
    panzoomContainer.instance.smoothZoomAbs(panzoomContainer.offsetWidth / 2, panzoomContainer.offsetHeight / 2, currentScale * 1.25)
  }

  zoomOut () {
    const activeSlide = this.element.querySelector('.swiper-slide-active')

    if (!activeSlide) {
      return
    }

    const panzoomContainer = activeSlide.querySelector('.panzoom-container')

    if (!panzoomContainer) {
      return
    }

    const currentScale = panzoomContainer.instance.getTransform().scale || 1
    panzoomContainer.instance.smoothZoomAbs(panzoomContainer.offsetWidth / 2, panzoomContainer.offsetHeight / 2, currentScale * 0.75)
  }

  handleZoomPan (event) {

  }

  onSwiperSlideChange () {
    if (!this.swiperWrapper || !this.swiperWrapper.swiper || !this.swiperWrapper.swiper.slides || this.element.classList.contains('lightbox--zoom-1')) {
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

    // Dispatch event to update 'image-header' slider:
    window.dispatchEvent(new CustomEvent('lightbox-slider-updated', { detail: this.swiperWrapper.swiper.activeIndex }))

    this.doInformationWrappers()
  }

  onSwiperChangeTransitionEnd () {
    // Reset panzoom on slide change
    this.panzoomContainers.forEach(container => {
      // somehow, moving and panning at the same time to the center seems to be a large issue with panzoom
      container.instance.setMinZoom(INITIAL_ZOOM)
      container.instance.setMaxZoom(INITIAL_ZOOM)
      container.instance.setTransformOrigin(null)
      container.instance.zoomTo(0, 0, INITIAL_ZOOM)
      container.instance.setMinZoom(MIN_ZOOM)
      container.instance.setMaxZoom(MAX_ZOOM)
      window.requestAnimationFrame(() => container.instance.moveTo(0, 0))
    })
  }

  doInformationWrappers () {
    const informationWrappers = [...this.element.querySelectorAll('.lightbox__information-wrapper')]

    if (!informationWrappers.length) {
      return
    }

    if (informationWrappers.length > 1) {
      informationWrappers.forEach(element => element.classList.remove('lightbox__information-wrapper--active'))
      const activeInfoContainer = informationWrappers[this.swiperWrapper.swiper.activeIndex]

      if (activeInfoContainer) {
        activeInfoContainer.classList.add('lightbox__information-wrapper--active')
      }
    } else {
      informationWrappers[0].classList.add('lightbox__information-wrapper--active')
    }
  }

  initAccessibility () {
    this.setAriaHiddenOnOtherElements(false)
    this.hideOverlayTabbableElements(true)

    this.overlayFocusTrap = focusTrap(this.element, {
      onActivate: () => { },
      onDeactivate: () => {
        this.toggleOverlay(true)

        if (this.buttonClose) {
          this.buttonClose.focus()
        }
      },
      escapeDeactivates: true,
      clickOutsideDeactivates: true,
      returnFocusOnDeactivate: false
    })
  }

  setAriaHiddenOnOtherElements (hidden = true) {
    const nonModalDialogVisibleElements = [...document.querySelectorAll('.content')]
    const modalDialogVisibleElements = [...document.querySelectorAll('.lightbox')]

    nonModalDialogVisibleElements.forEach(element => element.setAttribute('aria-hidden', hidden))
    modalDialogVisibleElements.forEach(element => element.setAttribute('aria-hidden', !hidden))
  }

  hideOverlayTabbableElements (hidden = true) {
    const modalDialogTabbableElements = [...document.querySelectorAll('.lightbox a[href]')]

    modalDialogTabbableElements.forEach(element => element.classList.toggle('is-hidden', hidden))

    if (hidden) {
      modalDialogTabbableElements.forEach(element => element.setAttribute('tabindex', -1))
    } else {
      modalDialogTabbableElements.forEach(element => element.removeAttribute('tabindex'))
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.lightbox').forEach(element => {
  element.instance = element.instance || new Lightbox(element)
}))
