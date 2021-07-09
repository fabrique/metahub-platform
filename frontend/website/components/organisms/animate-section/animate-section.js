
import AnimateSection from '../../../assets/scripts/modules/animate-section'
import Component from '../../../assets/scripts/modules/component'

class AnimateSectionComponent extends Component {
  init () {
    const section = this.element.querySelector('.js-animate-section')

    this.animateSection = new AnimateSection(section)
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-animate-section').forEach(element => {
  element.instance = element.instance || new AnimateSectionComponent(element)
}))
