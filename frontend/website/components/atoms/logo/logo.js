
import Component from '../../../assets/scripts/modules/component'

class LogoComponent extends Component {
  init () {
    this.frames = [...this.element.querySelectorAll('.logo-frame')]

    if (!this.frames.length) {
      return
    }

    this.frames.forEach(frame => frame.classList.add('logo-frame--hidden'))
    this.frames[this.frames.length * Math.random() | 0].classList.remove('logo-frame--hidden')
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.logo').forEach(element => {
  element.instance = element.instance || new LogoComponent(element)
}))
