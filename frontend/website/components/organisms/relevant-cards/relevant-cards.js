
import Component from '../../../assets/scripts/modules/component'
import TitleTween from '../../../assets/scripts/modules/title-tween'

class RelevantCardsComponent extends Component {
  init () {
    const title = this.element.querySelector('.js-relevant__title')

    this.tween = new TitleTween(title, 1, 2)
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-relevant-cards').forEach(element => {
  element.instance = element.instance || new RelevantCardsComponent(element)
}))
