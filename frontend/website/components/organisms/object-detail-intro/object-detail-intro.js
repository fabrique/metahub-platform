
import Component from '../../../assets/scripts/modules/component'

class ObjectDetailIntroComponent extends Component {
  init () {
    const title = this.element.querySelector('.object-detail__intro__titles')

    // TODO: TEMPORARILY DISABLED: this.tween = new TitleTween(title, 1, 4)
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.object-detail__intro').forEach(element => {
  element.instance = element.instance || new ObjectDetailIntroComponent(element)
}))
