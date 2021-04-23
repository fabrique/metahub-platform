
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
    // other classnames, for no conflict with multiple swipers MKR, connected by choice so nvm
    nextEl: '.swiper-button-next-di',
    prevEl: '.swiper-button-prev-di'
  }
}

let timeout

export default class DetailImage extends Component {
  init () {
    this.element = document.querySelector('.detail-image')
    this.observer = null
    this.container = this.element.querySelector('.swiper-container')
    this.favoriteButton = this.element.querySelector('.button-favorite')
    this.heartIcon = this.element.querySelector('.heart-icon')
    this.expandButton = this.element.querySelector('.expand-button')

    if (this.expandButton) {
      this.expandButton.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('open-lightbox'))
      })
    }

    if (this.container) {
      this.liveregion = document.createElement('div')
      this.liveregion.setAttribute('aria-live', 'polite')
      this.liveregion.setAttribute('aria-atomic', 'true')
      this.liveregion.setAttribute('class', 'liveregion visuallyhidden')
      this.container.appendChild(this.liveregion)
      this.liveregion.style.position = 'absolute'

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

      window.addEventListener('header-slider-updated', (event) => {
        this.swiperWrapper.swiper.slideTo(event.detail)
      })
      window.addEventListener('lightbox-slider-updated', (event) => {
        this.swiperWrapper.swiper.slideTo(event.detail)
      })
    }

    this.objectId = this.element.getAttribute('data-id')
    this.category = this.element.getAttribute('data-category')

    const isFavorited = this.isFavorited()

    if (isFavorited) {
      this.favoriteButton.classList.add('button-favorite--active')
    }

    this.favoriteButton.addEventListener('click', () => this.onToggleFavorite())

    window.addEventListener('toggle-favorited-mobile', () => {
      // console.log('mobile was (un)favorited')
      if (this.isFavorited()) {
        this.favoriteButton.classList.remove('button-favorite--active')
      } else {
        this.favoriteButton.classList.add('button-favorite--active')
      }
    })
  }

  isFavorited () {
    const favorites = JSON.parse(localStorage.getItem('favorites')) || {}

    if (favorites[this.category]) {
      const index = favorites[this.category].indexOf(this.objectId)
      return index !== -1
    }
    return false
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
    // Dispatch event to update 'image-header' slider: MKR: not sure if we want this but ok
    window.dispatchEvent(new CustomEvent('detail-slider-updated', { detail: this.swiperWrapper.swiper.activeIndex }))
  }

  onToggleFavorite () {
    // This favourite button is only shown on the mobile variant
    // The mobile variant is container in article.js
    // console.log('toggle-fav')
    // console.log(this.category)

    const favorites = JSON.parse(localStorage.getItem('favorites')) || {}

    let index = -1
    if (favorites[this.category]) {
      index = favorites[this.category].indexOf(this.objectId)
      // console.log('category existed')
    } else {
      favorites[this.category] = []
      // console.log('making category')
    }

    if (index === -1) {
      // console.log('add')
      favorites[this.category].push(this.objectId)
      // console.log(favorites)
      localStorage.setItem('favorites', JSON.stringify(favorites))

      this.favoriteButton.classList.add('article-detail__icon-favorite--active')
      window.dispatchEvent(new CustomEvent('toggle-favorited-desktop'))
    } else {
      // console.log('remove')
      favorites[this.category].splice(favorites[this.category].indexOf(this.objectId), 1)
      localStorage.setItem('favorites', JSON.stringify(favorites))

      // Somehow this stays on?
      // console.log(this.favoriteButton.classList)
      this.favoriteButton.classList.remove('article-detail__icon-favorite--active')
      // console.log('call remove')
      this.favoriteButton.classList.remove('button-favorite--active')
      // console.log(this.favoriteButton.classList)
      window.dispatchEvent(new CustomEvent('toggle-favorited-desktop'))
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.detail-image').forEach(element => {
  element.instance = element.instance || new DetailImage(element)
}))
