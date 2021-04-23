
import Component from '../../../assets/scripts/modules/component'

export default class SkipToMainComponent extends Component {
  init () {
    this.link = this.element.querySelector('.link')
    this.link.addEventListener('click', event => this.clickHandler(event))
  }

  clickHandler (event) {
    const target = document.querySelector('[role="main"]')
    const rect = target.getBoundingClientRect()

    window.scrollTo(0, rect.y)

    if (event) {
      event.preventDefault()
      event.stopPropagation()
    }

    window.requestAnimationFrame(() => this.link.blur())
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.skip-to-main').forEach(element => {
  element.instance = element.instance || new SkipToMainComponent(element)
}))
