
import { createFocusTrap } from 'focus-trap'

import Component from '../../../assets/scripts/modules/component'

export default class MenuBarComponent extends Component {
  init () {
    const width = 1180

    this.wrapper = this.element.querySelector('.menu-bar__wrapper')

    this.menuButton = this.element.querySelector('.js-menu-bar__menu-btn')
    this.links = this.element.querySelector('.js-menu-bar__links')
    this.menuBar = this.element.querySelector('.js-menu-bar')

    this.firstMenuItem = this.links.querySelector('.link')

    // Navigation dialog
    this.menuIsOpen = false
    this.menuButton.addEventListener('click', () => this.toggleMobileMenu())

    this.initAccessibility()

    // Menu breaks on larger resolutions, so force close it.

    window.addEventListener('resize', () => {
      if (window.innerWidth < width) {
        this.element.ariaLabel = 'Navigation dialog'
      }

      if (!this.menuIsOpen || this.isTogglingMenu || !this.oldWidth || window.innerWidth === this.oldWidth) {
        this.oldWidth = window.innerWidth
        return
      }

      this.oldWidth = window.innerWidth

      if (window.innerWidth < width) {
        return
      }

      this.toggleMobileMenu()
    }, { passive: true })
  }

  toggleMobileMenu () {
    if (this.isTogglingMenu) {
      return
    }

    this.isTogglingMenu = true

    if (!this.menuIsOpen) {
      this.links.classList.add('js-menu-bar__links--open')
      this.menuButton.classList.add('js-menu-bar__menu-btn--open')
      this.menuIsOpen = true
      this.menuButton.setAttribute('aria-expanded', 'true')
      this.links.removeAttribute('hidden')

      if (this.focusTrap) {
        this.setAriaHiddenOnOtherElements(true)
        this.hideOverlayTabbableElements(false)
        this.focusTrap.activate()
      }

      document.body.style.overflow = 'hidden'
      document.body.style.height = '100%'
      document.body.style.position = 'fixed'
      document.body.style.zIndex = '0'

      window.dispatchEvent(new CustomEvent('open-menu'))
    } else if (this.menuIsOpen) {
      this.links.classList.remove('js-menu-bar__links--open')
      this.menuButton.classList.remove('js-menu-bar__menu-btn--open')
      this.menuIsOpen = false
      this.menuButton.setAttribute('aria-expanded', 'false')
      this.links.hidden = true

      if (this.focusTrap) {
        this.focusTrap.deactivate()
      }

      document.body.style.overflow = 'visible'
      document.body.style.height = 'auto%'
      document.body.style.position = 'static'
      document.body.style.zIndex = '0'

      window.dispatchEvent(new CustomEvent('close-menu'))
    }

    this.isTogglingMenu = false
  }

  initAccessibility () {
    this.setAriaHiddenOnOtherElements(false)
    this.hideOverlayTabbableElements(true)

    this.focusTrap = createFocusTrap(this.wrapper, {
      onActivate: () => {
        this.firstMenuItem.focus()
        this.firstMenuItem.blur()
      },
      onDeactivate: () => {
        // this.menuIsOpen = true
        this.toggleMobileMenu()
        this.menuButton.focus()
      },
      escapeDeactivates: true,
      clickOutsideDeactivates: true,
      returnFocusOnDeactivate: false
    })
  }

  setAriaHiddenOnOtherElements (hidden = true) {
    const nonModalDialogVisibleElements = [...document.querySelectorAll('.content')]
    const modalDialogVisibleElements = [...document.querySelectorAll('.menu-overlay')]

    nonModalDialogVisibleElements.forEach(element => element.setAttribute('aria-hidden', hidden))
    modalDialogVisibleElements.forEach(element => element.setAttribute('aria-hidden', !hidden))
  }

  hideOverlayTabbableElements (hidden = true) {
    const modalDialogTabbableElements = [...document.querySelectorAll('.menu-overlay a[href], .menu-overlay button')]

    modalDialogTabbableElements.forEach(element => element.classList.toggle('is-hidden', hidden))

    if (hidden) {
      modalDialogTabbableElements.forEach(element => element.setAttribute('tabindex', -1))
    } else {
      modalDialogTabbableElements.forEach(element => element.removeAttribute('tabindex'))
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-menu-bar').forEach(element => {
  element.instance = element.instance || new MenuBarComponent(element)
}))
