
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
  }
}

let timeout

export default class ArticlePhotoCarouselComponent extends Component {
  init () {
    this.observer = null
    this.container = this.element.querySelector('.swiper-container')

    let swiperOptions = { ...SWIPER_OPTIONS }

    if ([...this.container.querySelectorAll('.swiper-slide')].length < 2) {
      swiperOptions = { ...swiperOptions, ...{ noSwipe: true, navigation: true, pagination: true, loop: false } }
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

    currentWithDuplicates.forEach(slide => {
      slide.classList.add('swiper-slide--activated')
    })
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.article-photo-carousel').forEach(element => {
  element.instance = element.instance || new ArticlePhotoCarouselComponent(element)
}))
