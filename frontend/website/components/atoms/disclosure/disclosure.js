
import Component from '../../../assets/scripts/modules/component'

class DisclosureComponent extends Component {
  init () {
    this.button = this.element.querySelector('.disclosure__title-button')
    this.region = this.element.querySelector('.disclosure__content-container')

    if (!this.button || !this.region) {
      return
    }

    this.button.addEventListener('click', () => this.toggleRegion())
  }

  toggleRegion () {
    if (this.button.getAttribute('aria-expanded') === 'true') {
      this.region.setAttribute('aria-hidden', true)
      this.button.setAttribute('aria-expanded', false)
    } else {
      this.region.setAttribute('aria-hidden', false)
      this.button.setAttribute('aria-expanded', true)

      const rect = this.region.getBoundingClientRect()
      window.scroll({ top: (window.pageYOffset + rect.top) - (window.innerHeight / 3), left: 0, behavior: 'smooth' })
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.disclosure').forEach(element => {
  element.instance = element.instance || new DisclosureComponent(element)
}))
