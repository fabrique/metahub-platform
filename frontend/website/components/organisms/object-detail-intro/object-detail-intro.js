
import Component from '../../../assets/scripts/modules/component'
import TitleTween from '../../../assets/scripts/modules/title-tween'

class ObjectDetailComponent extends Component {
  init () {
    const title = this.element.querySelector('.js-object-detail__intro__title')
    const wrapper = '.js-object-detail__intro'
    const smallerThanLandscape = window.innerWidth < 800

    this.tween = new TitleTween({
      element: title,
      wrapper: wrapper,
      start: 1,
      end: 2,
      startTrigger: smallerThanLandscape ? 'bottom bottom' : 'top top'
    })
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-object-detail__intro').forEach(element => {
  element.instance = element.instance || new ObjectDetailComponent(element)
}))
