
import Component from '../../../assets/scripts/modules/component'
import onScrollChange from '../../../assets/scripts/utilities/on-scroll-change'

export default class ObjectDetails extends Component {
  init () {
    this.objectDetails = document.querySelector('.object-details')
    this.dropdowns = this.objectDetails.querySelectorAll('.object-details__dropdown')
    this.firstContainer = this.objectDetails.querySelectorAll('.object-details__information-container')[0]
    this.titleContainer = this.objectDetails.querySelectorAll('.object-details__title-container')[0]
    this.initDropdowns()
    this.initFavourite()

    this.vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
    this.vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)

    const isMobile = window.matchMedia('(max-width: 800px)').matches
    if (!isMobile && document.body.classList.contains('transition-animated')) {
      this.initAnimations()
    }
  }

  initFavourite () {
    this.favoriteButton = this.element.querySelector('.object-details__icon-favorite')
    // console.log(this.favoriteButton)

    this.objectId = this.element.getAttribute('data-id')
    this.category = this.element.getAttribute('data-category')
    const isFavorited = this.isFavorited()

    if (this.favoriteButton) {
      this.favoriteButton.addEventListener('click', () => this.onToggleFavorite())

      if (isFavorited) {
        this.favoriteButton.classList.add('object-details__icon-favorite--active')
      }
    } else {
      return
    }

    // Toggle this too if the desktop version was favourited
    window.addEventListener('toggle-favorited-desktop', () => {
      // console.log('desktop was (un)favorited')
      if (this.isFavorited()) {
        this.favoriteButton.classList.remove('object-details__icon-favorite--active')
      } else {
        this.favoriteButton.classList.add('object-details__icon-favorite--active')
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

  onToggleFavorite () {
    // This favourite button is only shown on the mobile variant
    // The desktop variant is container in detail-image.js
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

      this.favoriteButton.classList.add('object-details__icon-favorite--active')
      window.dispatchEvent(new CustomEvent('toggle-favorited-mobile'))
    } else {
      // console.log('remove')
      favorites[this.category].splice(favorites[this.category].indexOf(this.objectId), 1)
      localStorage.setItem('favorites', JSON.stringify(favorites))

      // Somehow this stays on?
      // console.log(this.favoriteButton.classList)
      this.favoriteButton.classList.remove('object-details__icon-favorite--active')
      // console.log('call remove')
      this.favoriteButton.classList.remove('button-favorite--active')
      // console.log(this.favoriteButton.classList)
      window.dispatchEvent(new CustomEvent('toggle-favorited-mobile'))
    }
  }

  initAnimations () {
    this.headerImage = document.querySelector('.image-header--context')
    this.articleDetailImage = document.querySelector('.article-detail__main-image .swiper-container')
    this.articleDetailImageContainer = document.querySelector('.article-detail__main-image')
    this.contextRibbon = document.querySelector('.context-cards-overlay__ribbon')
    this.contextOffset = this.contextRibbon.offsetTop
    this.relatedObjects = document.querySelector('.related-objects')
    this.initTargetCSSValues()
    onScrollChange(() => { this.animationTimeLine() })
  }

  initTargetCSSValues () {
    const sourcedata = this.headerImage.getBoundingClientRect()
    this.source_x = sourcedata.x
    this.source_w = sourcedata.width
    this.source_h = sourcedata.height
    const targetdata = this.articleDetailImage.getBoundingClientRect()
    this.target_x = targetdata.x
    this.target_y = targetdata.y - 50 // the end value of scroll animations with some offset for tweaking
    this.target_w = targetdata.width
    this.target_h = targetdata.height
    // set the width on ther target image, since fixed makes it bleed everywhere
    this.articleDetailImage.style.width = targetdata.width + 'px'
    this.animationStart = this.contextOffset + 250// 250 pixel scrolled upwards then start

    // end of stickyness at bottom of page
    this.endSticky = this.relatedObjects.getBoundingClientRect().y - this.vh // substract viewport height, so this value is when it enters the viewport
    this.articleDetailOffset = document.querySelector('.article-detail').getBoundingClientRect().y
  }

  animateImage (yo) {
    // get left offset of destination
    if (yo > this.target_y) {
      document.body.classList.add('image_animatin_endstate')
      return
    } else {
      document.body.classList.remove('image_animatin_endstate')
    }

    // set the image as background, to solve nonresizing of swiper and the image squishing on resize
    // also it's silly to animate a swiper instance, heavy load much

    const workimage = this.headerImage.querySelector('.swiper-slide-active .picture__image')
    // console.log(workimage.getAttribute('src'))
    // TODO do this only once
    this.headerImage.style.backgroundImage = `url(${workimage.getAttribute('src')})`

    // put percentage based on travel distance
    const distance = this.target_y - this.animationStart
    const travel = this.target_y - yo // y offset in scroll
    const percentage = ((distance - travel) / distance)
    // calculate values
    const scalew = 1 - ((1 - (this.target_w / this.source_w)) * percentage)
    const scaleh = 1 - ((1 - (this.target_h / this.source_h)) * percentage)
    const newWidth = this.source_w * scalew
    const newHeight = this.source_h * scaleh
    const ax = (this.target_x * percentage)
    const ay = (-55 * percentage) // offset to top by some pixels, since we are pushed down somewhat for the header
    // this.headerImage.style.transform = 'translate3D(' + ax + 'px, ' + ay + 'px, 0px) scale(' + scalew + ',' + scaleh + ')'
    this.headerImage.style.transform = `translate3D(${ax}px, ${ay}px, 0px)`
    this.headerImage.style.width = newWidth + 'px'
    this.headerImage.style.height = newHeight + 'px'
  }

  animationTimeLine () {
    // match media for mobile

    if (window.scrollY >= this.endSticky) {
      if (!document.body.classList.contains('image_notsticky_endstate')) {
        document.body.classList.add('image_notsticky_endstate')
        this.articleDetailImageContainer.style.top = (window.scrollY - this.vh) + 'px'
      }
    } else if (window.scrollY >= this.animationStart) {
      document.body.classList.add('image_animatin') // add to body to easier compensate the fixed element void of 126 pixels...
      if (document.body.classList.contains('image_notsticky_endstate')) {
        document.body.classList.remove('image_notsticky_endstate')
        this.articleDetailImageContainer.style.top = ''
      }
      this.animateImage(window.scrollY)
    } else {
      if (document.body.classList.contains('image_animatin')) {
        document.body.classList.remove('image_animatin')
        this.headerImage.style.transform = 'translate3D(0px, 0px, 0px)'
        this.headerImage.style.width = ''
        this.headerImage.style.height = ''
      }
    }
  }

  initDropdowns () {
    if (this.firstContainer) {
      this.firstContainer.classList.add('object-details__information-container--active')
    }

    if (this.titleContainer) {
      this.titleContainer.setAttribute('aria-expanded', 'true')
    }

    this.dropdowns.forEach(item => {
      item.addEventListener('click', event => this.toggleDropdown(event))
    })
  }

  toggleDropdown (event) {
    const informationContainer = event.target.querySelector('.object-details__information-container')
    const arrow = event.target.querySelector('.object-details__dropdown-arrow')
    const titleContainer = event.target.querySelector('.object-details__title-container')

    if (!informationContainer) {
      return
    }
    if (informationContainer.classList.contains('object-details__information-container--active')) {
      informationContainer.classList.remove('object-details__information-container--active')
      arrow.classList.remove('object-details__dropdown-arrow--inverted')
      titleContainer.setAttribute('aria-expanded', 'false')
    } else {
      informationContainer.classList.add('object-details__information-container--active')
      arrow.classList.add('object-details__dropdown-arrow--inverted')
      titleContainer.setAttribute('aria-expanded', 'true')
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.object-details').forEach(element => {
  element.instance = element.instance || new ObjectDetails(element)
}))
