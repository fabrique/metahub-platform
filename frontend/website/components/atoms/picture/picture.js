
import Component from '../../../assets/scripts/modules/component'

class PictureComponent extends Component {
  init () {
    this.img = this.element.querySelector('img')
    this.sourceElements = this.element.querySelectorAll('source')

    if (!this.img || !this.sourceElements.length) {
      return
    }

    this.sources = []
    this.sourceElements.forEach(source => this.sources.push({ src: source.srcset, media: source.media || 'screen', style: { objectFit: source.style.objectFit, objectPosition: source.style.objectPosition } }))

    this.addMediaQueryListeners()
    this.applySource(this.sources.find(source => window.matchMedia(source.media).matches))

    if (this.img.currentSrc) {
      this.element.classList.add('picture--loaded')
    } else {
      this.img.addEventListener('load', this.onImageLoad.bind(this))
    }
  }

  applySource (source) {
    if (source.style.objectFit !== undefined) {
      this.img.style.objectFit = source.style.objectFit
    }

    if (source.style.objectPosition !== undefined) {
      this.img.style.objectPosition = source.style.objectPosition
    }
  }

  addMediaQueryListeners () {
    this.sources.forEach(source => window.matchMedia(source.media).addListener(
      result => result.matches && this.applySource(source)
    ))
  }

  onImageLoad () {
    this.element.classList.add('picture--loaded')
    this.img.removeEventListener('load', this.onImageLoad.bind(this))
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.picture').forEach(element => {
  element.instance = element.instance || new PictureComponent(element)
}))

window.addEventListener('re-init-images', () => document.querySelectorAll('.picture').forEach(element => {
  element.instance = element.instance || new PictureComponent(element)
}))
