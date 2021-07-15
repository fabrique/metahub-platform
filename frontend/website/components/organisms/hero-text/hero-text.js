
import Component from '../../../assets/scripts/modules/component'
import TitleTween from '../../../assets/scripts/modules/title-tween'

class HeroTextComponent extends Component {
  init () {
    const title = this.element.querySelector('.js-hero-text__title')
    const wrapper = '.js-hero-text'

    this.tween = new TitleTween({
      element: title,
      wrapper: wrapper,
      start: 1,
      end: 2,
      startTrigger: 'top top'
    })
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-hero-text').forEach(element => {
  element.instance = element.instance || new HeroTextComponent(element)
}))
