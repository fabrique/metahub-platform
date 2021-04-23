
import Component from '../../../assets/scripts/modules/component'

class ScrollDownButtonComponent extends Component {
  init () {
    if ('scrollBehavior' in document.documentElement.style) {
      return
    }

    this.element.addEventListener('click', event => this.onClickHandler(event))
  }

  onClickHandler (event) {
    const target = document.querySelector('#main')

    if (!target) {
      // Fallback - If we don't have a target, assume that we want to scroll exactly one screen height from the top.
      window.scroll({ top: window.innerHeight, behavior: 'smooth' })
    } else {
      // Regular behavior - Scroll to the main element.
      target.scrollIntoView({ behavior: 'smooth' })
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.scroll-down-button').forEach(element => {
  element.instance = element.instance || new ScrollDownButtonComponent(element)
}))
