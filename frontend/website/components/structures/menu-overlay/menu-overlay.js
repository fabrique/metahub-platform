
import { createFocusTrap } from 'focus-trap'
import throttle from 'lodash/throttle'

import Component from '../../../assets/scripts/modules/component'

export default class MenuOverlayComponent extends Component {
  init () {
    this.overlay = document.querySelector('.menu-overlay')
    this.buttonClose = this.overlay.querySelector('.button--close')

    this.initAccessibility()
    this.initOverlay()
  }

  initOverlay () {
    const throttledToggle = throttle(() => window.requestAnimationFrame(() => this.toggleOverlay()), 350, { leading: true, trailing: true })

    this.buttonClose.addEventListener('click', () => throttledToggle())
    window.addEventListener('open-menu-overlay', () => throttledToggle())
  }

  toggleOverlay (forceClose = false) {
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

  initAccessibility () {
    this.setAriaHiddenOnOtherElements(false)
    this.hideOverlayTabbableElements(true)

    this.overlayFocusTrap = createFocusTrap(this.overlay, {
      onActivate: () => {},
      onDeactivate: () => {
        this.toggleOverlay(true)
        this.buttonClose.focus()
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
    const modalDialogTabbableElements = [...document.querySelectorAll('.menu-overlay a[href]')]

    modalDialogTabbableElements.forEach(element => element.classList.toggle('is-hidden', hidden))

    if (hidden) {
      modalDialogTabbableElements.forEach(element => element.setAttribute('tabindex', -1))
    } else {
      modalDialogTabbableElements.forEach(element => element.removeAttribute('tabindex'))
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.menu-overlay').forEach(element => {
  element.instance = element.instance || new MenuOverlayComponent(element)
}))
