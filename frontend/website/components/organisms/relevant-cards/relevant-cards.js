
import Component from '../../../assets/scripts/modules/component'
import TitleTween from '../../../assets/scripts/modules/title-tween'

class RelevantCardsComponent extends Component {
  init () {
    const title = this.element.querySelector('.js-relevant__title')
    const wrapper = '.js-relevant-cards'

    this.tween = new TitleTween({
      element: title,
      wrapper: wrapper,
      start: 2,
      end: 1,
      endTrigger: 'bottom bottom'
    })
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-relevant-cards').forEach(element => {
  element.instance = element.instance || new RelevantCardsComponent(element)
}))
