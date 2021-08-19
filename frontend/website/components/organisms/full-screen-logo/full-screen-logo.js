
import Component from '../../../assets/scripts/modules/component'

class FullScreenLogoComponent extends Component {
  init () {
    this.frames = [...this.element.querySelectorAll('.full-logo-frame')]

    if (!this.frames.length) {
      return
    }

    this.frames.forEach(frame => frame.classList.add('full-logo-frame--hidden'))
    this.frames[this.frames.length * Math.random() | 0].classList.remove('full-logo-frame--hidden')
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.full-screen-logo').forEach(element => {
  element.instance = element.instance || new FullScreenLogoComponent(element)
}))
