
import Component from '../../../assets/scripts/modules/component'

class FormComponent extends Component {
  init () {
    this.submitButton = this.element.querySelector('button[type="submit"], input[type="submit"]')
    this.element.addEventListener('submit', this.preventMultipleSubmits.bind(this))
  }

  preventMultipleSubmits () {
    this.submitButton.disabled = true
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.form').forEach(element => {
  element.instance = element.instance || new FormComponent(element)
}))
