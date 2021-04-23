
import Component from '../../../assets/scripts/modules/component'
import fireCustomEvent from '../../../assets/scripts/utilities/fire-custom-event'

export default class ArticleCookiesComponent extends Component {
  init () {
    this.observedIntersectionElements = this.element.querySelectorAll('.article-cookies__title, .article-cookies__text, .article-cookies__buttons')

    this.buttonChange = this.element.querySelector('.button--change')
    this.buttonClear = this.element.querySelector('.button--clear')

    this.buttonChange.addEventListener('click', event => {
      event.preventDefault()
      fireCustomEvent('show-cookie-details')
    })

    this.buttonClear.addEventListener('click', event => {
      event.preventDefault()
      fireCustomEvent('clear-cookie-settings')
    })
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.article-cookies').forEach(element => {
  element.instance = element.instance || new ArticleCookiesComponent(element)
}))
