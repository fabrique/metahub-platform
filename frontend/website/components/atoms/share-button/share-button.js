
import Component from '../../../assets/scripts/modules/component'

const POPUP_WIDTH = 800
const POPUP_HEIGHT = 480
const CENTER_POPUP = true

class ShareButtonComponent extends Component {
  init () {
    this.href = this.element.getAttribute('href')
    this.span = this.element.querySelector('.share-button__span')
    this.title = this.span ? this.span.innerText : ''

    this.element.addEventListener('click', event => this.onClickHandler(event))
  }

  onClickHandler (event) {
    if (this.element.getAttribute('data-open-popup') !== null && this.openSharePopup()) {
      event.preventDefault()
    }
  }

  openSharePopup () {
    const width = Math.max(window.innerWidth / 2, POPUP_WIDTH)
    const height = Math.max(window.innerHeight / 2, POPUP_HEIGHT)
    const top = (window.outerHeight / 2) - (height / 2)
    const left = (window.outerWidth / 2) - (width / 2)

    return window.open(this.href, this.title, (CENTER_POPUP ? `top=${top}, left=${left}, ` : '') + `height=${height}, width=${width}, outerWidth=${width}, outerHeight=${height}, menubar=0, toolbar=0, location=0, personalbar=0, status=0, minimizable=1, resizable=1, scrollbar=1`)
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.share-button').forEach(element => {
  element.instance = element.instance || new ShareButtonComponent(element)
}))
