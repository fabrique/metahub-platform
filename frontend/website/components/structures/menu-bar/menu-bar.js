
import Component from '../../../assets/scripts/modules/component'
import onScrollChange from '../../../assets/scripts/utilities/on-scroll-change'

export default class MenuBarComponent extends Component {
  init () {
    this.menu = this.element
    this.sticky = this.element.querySelector('.menu-bar__nav-bar').offsetTop
    this.menuButton = this.element.querySelector('.menu-bar__menu-btn')
    this.links = this.element.querySelector('.menu-bar__links')
    this.mobileLinks = this.element.querySelector('.menu-bar__links-mobile')
    this.favoriteLink = this.element.querySelector('.menu-bar__favorites-link')
    this.favoriteIcon = this.favoriteLink.querySelector('.link__icon--after')

    this.menuIsOpen = false
    this.menuButton.addEventListener('click', () => this.toggleMobileMenu())

    onScrollChange(() => { this.makeStickyMenu() })

    window.addEventListener('toggle-favorited-mobile', () => this.updateFavorites())
    window.addEventListener('toggle-favorited-desktop', () => this.updateFavorites())

    this.updateFavorites()

    // Menu breaks on larger resolutions, so force close it.
    window.addEventListener('resize', () => {
      if (!this.menuIsOpen || this.isTogglingMenu || !this.oldWidth || window.innerWidth === this.oldWidth) {
        this.oldWidth = window.innerWidth
        return
      }

      this.oldWidth = window.innerWidth

      if (window.innerWidth < 800) {
        return
      }

      this.toggleMobileMenu()
    }, { passive: true })
  }

  updateFavorites () {
    const favorites = JSON.parse(localStorage.getItem('favorites'))

    let numberOfFavorites = 0
    if (favorites) {
      const stories = favorites.story ? favorites.story.length : 0
      const object = favorites.object ? favorites.object.length : 0
      const series = favorites.series ? favorites.series.length : 0
      numberOfFavorites = (stories + object + series) // eslint-disable-line smells/no-complex-string-concat
    }

    const badge = this.element.querySelector('.menu-bar__favorites-badge')

    if (numberOfFavorites > 0) {
      if (badge) {
        badge.remove()
        const createdBadge = document.createElement('span')
        const number = document.createTextNode(numberOfFavorites)
        createdBadge.appendChild(number)
        createdBadge.classList.add('menu-bar__favorites-badge')
        this.favoriteIcon.appendChild(createdBadge)
      } else {
        const createdBadge = document.createElement('span')
        const number = document.createTextNode(numberOfFavorites)
        createdBadge.appendChild(number)
        createdBadge.classList.add('menu-bar__favorites-badge')
        this.favoriteIcon.appendChild(createdBadge)
      }
    } else if (numberOfFavorites === 0) {
      if (badge) {
        badge.remove()
      }
    }
  }

  makeStickyMenu () {
    // match media for mobile
    const isMobile = window.matchMedia('(max-width: 800px)').matches
    if (!isMobile) {
      if (window.scrollY >= (this.sticky - 10)) { // 10 pixel offset
        document.body.classList.add('menu-bar--sticky') // add to body to easier compensate the fixed element void of 126 pixels...
      } else {
        document.body.classList.remove('menu-bar--sticky')
      }
    }
  }

  toggleMobileMenu () {
    if (this.isTogglingMenu) {
      return
    }

    this.isTogglingMenu = true

    if (!this.menuIsOpen) {
      this.mobileLinks.classList.add('menu-bar__links-mobile--open')
      this.menuIsOpen = true
      this.menuButton.setAttribute('aria-expanded', 'true')
      this.mobileLinks.removeAttribute('hidden')

      document.body.style.overflow = 'hidden'
      document.body.style.height = '100%'
      document.body.style.position = 'fixed'
      document.body.style.zIndex = '0'

      window.dispatchEvent(new CustomEvent('open-menu'))
    } else if (this.menuIsOpen) {
      this.mobileLinks.classList.remove('menu-bar__links-mobile--open')
      this.menuIsOpen = false
      this.menuButton.setAttribute('aria-expanded', 'false')
      this.mobileLinks.hidden = true

      document.body.style.overflow = 'visible'
      document.body.style.height = 'auto%'
      document.body.style.position = 'static'
      document.body.style.zIndex = '0'

      window.dispatchEvent(new CustomEvent('close-menu'))
    }

    this.isTogglingMenu = false
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.menu-bar').forEach(element => {
  element.instance = element.instance || new MenuBarComponent(element)
}))
