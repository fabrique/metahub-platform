import Component from '../../../assets/scripts/modules/component'
import SwiperWrapper from '../../../assets/scripts/modules/swiper-wrapper'

const SWIPER_OPTIONS = {
  slidesPerView: 'auto',
  spaceBetween: 30,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev'
  }
}

let timeout

export default class ImageHeader extends Component {
  init () {
    this.observer = null
    this.container = this.element.querySelector('.swiper-container')
    this.expandButton = this.element.querySelector('.image-header__expand')

    if (this.expandButton) {
      this.expandButton.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('open-lightbox'))
      })
    }

    this.element.addEventListener('click', () => {
      const isMobile = window.matchMedia('(max-width: 800px)').matches
      if (isMobile) {
        window.dispatchEvent(new CustomEvent('open-lightbox'))
      }
    })

    if (this.container) {
      this.liveregion = document.createElement('div')
      this.liveregion.setAttribute('aria-live', 'polite')
      this.liveregion.setAttribute('aria-atomic', 'true')
      this.liveregion.setAttribute('class', 'liveregion visuallyhidden')
      this.container.appendChild(this.liveregion)
      this.liveregion.style.position = 'absolute'
      this.liveregion.style.opacity = '0'

      let swiperOptions = { ...SWIPER_OPTIONS }

      // remove buttons if there is only one
      if ([...this.container.querySelectorAll('.swiper-slide')].length < 2) {
        swiperOptions = {
          ...swiperOptions, ...{ noSwipe: true, navigation: true, loop: true }
        }
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

      window.addEventListener('detail-slider-updated', (event) => {
        this.swiperWrapper.swiper.slideTo(event.detail)
      })
      window.addEventListener('lightbox-slider-updated', (event) => {
        this.swiperWrapper.swiper.slideTo(event.detail)
      })
    }
  }

  onSwiperSlideChange () {
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

    // Dispatch event to update 'detail-image' slider:
    window.dispatchEvent(new CustomEvent('header-slider-updated', { detail: this.swiperWrapper.swiper.activeIndex }))
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.image-header').forEach(element => {
  element.instance = element.instance || new ImageHeader(element)
}))
