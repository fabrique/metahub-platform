
import Component from '../../../assets/scripts/modules/component'

export default class ObjectSeries extends Component {
  init () {
    this.objects = this.element.querySelectorAll('.object-series__object-card')
    this.objects.forEach(objectCard => objectCard.addEventListener('click', () => {
      window.dispatchEvent(new CustomEvent('open-lightbox--objects', { detail: 'test' }))
    }))
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.object-series').forEach(element => {
  element.instance = element.instance || new ObjectSeries(element)
}))
