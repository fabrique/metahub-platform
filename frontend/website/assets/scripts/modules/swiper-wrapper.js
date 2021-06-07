
// TODO: Clean this up!

const DEFAULT_SWIPER_OPTIONS = {
  autoPlay: false,
  controlBy: 'container',
  direction: 'horizontal',
  effect: 'slide',
  grabCursor: true,
  initialSlide: 0,
  loop: false,
  loopAdditionalSlides: 0,
  navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
  pagination: { el: '.swiper-pagination', type: 'bullets', bulletElement: 'span', clickable: true },
  paginationClickable: true,
  preloadImages: false,
  resistanceRatio: 0,
  roundLengths: true,
  slidesPerView: 1,
  spaceBetween: 0,
  threshold: 5,
  touchRatio: 1,
  watchOverflow: true
}

const OBSERVER_DELAY = 350

const DEFAULT_INTERSECT_HOOKS = [] // eslint-disable-line no-unused-vars

/*
const DEFAULT_INTERSECT_HOOKS = [
  {
    querySelector: '.background-image',
    callback: (change, element) => {
      if (change.isIntersecting && element.forceLoad && typeof element.forceLoad === 'function') {
        element.forceLoad()
      }
    }
  },

  {
    querySelector: '.background-video',
    callback: (change, element) => {
      if (change.isIntersecting && element.forceLoad && typeof element.forceLoad === 'function') {
        element.forceLoad()
      }

      if (change.isIntersecting && element.forcePlay && typeof element.forcePlay === 'function') {
        element.forcePlay()
      } else if (!change.isIntersecting && element.forcePause && typeof element.forcePause === 'function') {
        element.forcePause()
      }
    }
  }
]
*/

export default class SwiperWrapper {
  constructor (element, options = {}, intersectHooks = [], swiperEvents = {}, callback = () => {}) {
    this.element = element
    this.options = { ...DEFAULT_SWIPER_OPTIONS, ...options }
    this.intersectHooks = [].concat(intersectHooks) // No [...] array spread - this adds 100KB with current browserslist settings!
    this.swiperEvents = swiperEvents
    this.swiper = null
    this.observer = null

    this.init(callback)

    return this
  }

  async init (callback = () => {}) {
    const Swiper = (await import('../plugins/swiper')).default()

    this.swiper = new Swiper(this.element, this.options)

    if (this.swiperEvents) {
      Object.entries(this.swiperEvents).forEach(item => this.swiper.on(item[0], item[1]))
    }

    window.requestAnimationFrame(() => this.swiper.update())

    function attachObservers () {
      this.intersectHooks.forEach(hook => {
        this.element.querySelectorAll(hook.querySelector).forEach(element => {
          if (element && element.disconnectObservers && typeof element.disconnectObservers === 'function') {
            element.disconnectObservers() // Remove original observer
          }

          window.requestAnimationFrame(() => hook.callback({ isIntersecting: false }, element))
        })
      })

      window.requestAnimationFrame(() => this.attachObserver())
    }

    if (this.intersectHooks.length) {
      this.observer = null
      window.setTimeout(() => attachObservers(), OBSERVER_DELAY)
    }

    callback.apply(this)
  }

  update () {
    //
  }

  destroy () {
    this.observer = null
  }

  attachObserver () {
    if (this.observer) {
      this.disconnectObserver()
    }

    // Start halfway outside the viewport
    this.observer = new window.IntersectionObserver(this.onIntersect.bind(this), { root: this.element, rootMargin: '-2px -2px' })

    Object.values(this.swiper.slides).filter(value => value.classList).forEach(slide => this.observer.observe(slide))
  }

  disconnectObserver () {
    if (!this.observer) {
      return
    }

    this.observer.disconnect()
    this.observer = null
  }

  onIntersect (changes = []) {
    changes.forEach(change => {
      this.intersectHooks.forEach(hook => {
        const element = change.target.querySelector(hook.querySelector)

        if (element && hook.callback && typeof hook.callback === 'function') {
          hook.callback(change, element)
        }
      })
    })
  }
}
