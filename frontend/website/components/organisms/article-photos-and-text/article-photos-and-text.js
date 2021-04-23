
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

export default class PhotosAndText extends Component {
  init () {
    this.observer = null
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
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.article-photos-and-text').forEach(element => {
  element.instance = element.instance || new PhotosAndText(element)
}))
