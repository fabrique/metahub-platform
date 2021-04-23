
import Component from '../../../assets/scripts/modules/component'

export default class GridOverlay extends Component {
  init () {
    this.gridOverlay = this.element.querySelector('.grid-overlay')

    // eslint-disable-next-line no-undef
    // Check for production mode, disabled for now
    // if (process.env.NODE_ENV !== 'production') {
    document.addEventListener('keydown', (e) => this.showGridOverlay(e))
  }
  // }

  showGridOverlay (e) {
    if (e.key === 'l') {
      this.gridOverlay.classList.toggle('grid-overlay-visible')
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.content').forEach(element => {
  element.instance = element.instance || new GridOverlay(element)
}))
