
import Component from '../../../assets/scripts/modules/component'
import TitleTween from '../../../assets/scripts/modules/title-tween'

class PlacesMapComponent extends Component {
  init () {
    const title = this.element.querySelector('.js-places-map__title')
    const wrapper = '.js-places-map'

    this.tween = new TitleTween({
      element: title,
      wrapper: wrapper,
      start: 2,
      end: 1,
      endTrigger: 'bottom bottom'
    })

    this.buttonZoomIn = this.element.querySelector('.places-map__zoom-button--in')
    this.buttonZoomOut = this.element.querySelector('.places-map__zoom-button--out')
    this.svg = this.element.querySelector('.places-map__svg')

    if (this.buttonZoomIn) {
      this.buttonZoomIn.addEventListener('click', () => {
        if (this.element.classList.contains('places-map--zoomed-in')) {
          //
        } else {
          this.element.classList.add('places-map--zoomed-in')
          this.buttonZoomIn.disabled = true
          this.buttonZoomOut.disabled = false
        }
      })
    }

    if (this.buttonZoomOut) {
      this.buttonZoomOut.addEventListener('click', () => {
        if (this.element.classList.contains('places-map--zoomed-in')) {
          this.element.classList.remove('places-map--zoomed-in')
          this.buttonZoomOut.disabled = true
          this.buttonZoomIn.disabled = false
        } else {
          //
        }
      })
    }

    window.addEventListener('resize', () => this.onResize())
    this.onResize()
  }

  onResize () {
    if (!this.svg) {
      return
    }

    if (window.innerWidth < 800) {
      this.svg.setAttribute('viewBox', '400 0 2783 1785')
    } else {
      this.svg.setAttribute('viewBox', '0 0 2783 1785')
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.js-places-map').forEach(element => {
  element.instance = element.instance || new PlacesMapComponent(element)
}))
