
import Component from '../../../assets/scripts/modules/component'
import TitleTween from '../../../assets/scripts/modules/title-tween'

class RelevantCardsComponent extends Component {
  init () {
    const title = this.element.querySelector('.js-relevant__title')
    const wrapper = '.js-relevant-cards'

    this.tween = new TitleTween(title, wrapper, 2, 1)
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-relevant-cards').forEach(element => {
  element.instance = element.instance || new RelevantCardsComponent(element)
}))
