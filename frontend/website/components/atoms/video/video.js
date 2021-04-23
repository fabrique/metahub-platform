
import Component from '../../../assets/scripts/modules/component'

class VideoComponent extends Component {
  init () {
    this.video = this.element.querySelector('video')
    this.hitTarget = this.element.querySelector('.video__hit-target')

    if (!this.video || !this.hitTarget) {
      return
    }

    this.hitTarget.addEventListener('click', this.onHitTargetClick.bind(this))
    this.video.addEventListener('click', this.onHitTargetClick.bind(this))

    this.video.addEventListener('play', () => this.setClassesPlaying())
    this.video.addEventListener('pause', () => this.setClassesPaused())

    this.autoplay = (this.video.getAttribute('autoplay') !== null)

    if (this.autoplay) {
      this.setClassesPlaying()
    }
  }

  setClassesPlaying () {
    this.element.classList.remove('video--paused')
    this.element.classList.add('video--playing')
  }

  setClassesPaused () {
    this.element.classList.remove('video--playing')
    this.element.classList.add('video--paused')
  }

  onHitTargetClick (event) {
    event.preventDefault()

    if (this.video.currentTime === 0 || this.video.paused || this.video.ended) {
      this.video.play()
    } else {
      this.video.pause()
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.video').forEach(element => {
  element.instance = element.instance || new VideoComponent(element)
}))
