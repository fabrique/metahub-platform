
import Component from '../../../assets/scripts/modules/component'

class RelevantCardsComponent extends Component {
  init () {
    const title = this.element.querySelector('.relevant-objects__title, .relevant-stories__title, .relevant-news__title')

    // TODO: TEMPORARILY DISABLED: this.tween = new TitleTween(title, 1, 2)
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.relevant-objects, .relevant-stories, .relevant-news').forEach(element => {
  element.instance = element.instance || new RelevantCardsComponent(element)
}))
