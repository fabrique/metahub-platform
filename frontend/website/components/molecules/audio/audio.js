
import Component from '../../../assets/scripts/modules/component'
export default class ArticleAudioComponent extends Component {
  init () {
    this.observer = null
    this.button = this.element.querySelector('.audio__button')
    this.playButton = this.element.querySelector('.audio__play-button')
    this.pauseButton = this.element.querySelector('.audio__pause-button')
    this.audio = this.element.querySelector('.audio__audio')
    this.currentTime = this.element.querySelector('.audio__current-time')
    this.isPlaying = false

    this.button.addEventListener('click', () => this.onButtonClick())
    this.audio.addEventListener('timeupdate', () => this.onUpdateTime())

    // console.log('AUDIO', this.audio)

    this.audio.onloadedmetadata = () => {
      // console.log('loaded')
      const totalSeconds = this.audio.duration.toFixed(0)
      const minutes = Math.floor(totalSeconds / 60)
      const seconds = totalSeconds - minutes * 60
      this.currentTime.textContent = `${minutes}:${seconds < 10 ? 0 : ''}${seconds}`
    }
  }

  onButtonClick () {
    if (!this.isPlaying) {
      this.audio.play()
      this.isPlaying = true
      this.playButton.classList.add('audio__button--hide')
      this.pauseButton.classList.remove('audio__button--hide')
    } else {
      this.audio.pause()
      this.isPlaying = false
      this.playButton.classList.remove('audio__button--hide')
      this.pauseButton.classList.add('audio__button--hide')
    }
  }

  onUpdateTime () {
    const totalSeconds = this.audio.currentTime.toFixed(0)
    const minutes = Math.floor(totalSeconds / 60)
    const seconds = totalSeconds - minutes * 60
    this.currentTime.textContent = `${minutes}:${seconds < 10 ? 0 : ''}${seconds}`
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.audio').forEach(element => {
  element.instance = element.instance || new ArticleAudioComponent(element)
}))
