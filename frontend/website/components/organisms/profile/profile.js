
import Component from '../../../assets/scripts/modules/component'
import sleep from '../../../assets/scripts/utilities/sleep'

const WORDS_INTERVAL = 3000

class Profile extends Component {
  init () {
    this.container = this.element.querySelector('.profile__themes')
    this.button = this.element.querySelector('.profile__refresh-button')

    if (!this.container || !this.button) {
      return
    }

    this.pictureContainers = [...this.element.querySelectorAll('.profile__picture-container')]
    this.backgroundImages = [...this.element.querySelectorAll('.profile__background-image')]

    this.activeProfile = 1
    this.resize()

    this.button.addEventListener('click', () => this.cycleProfile())
    window.addEventListener('resize', () => this.resize())

    this.words = [...this.element.querySelectorAll('.profile__title-word')]

    if (this.words.length) {
      window.requestAnimationFrame(() => this.rotateWords())
    }
  }

  cycleProfile () {
    if (this.activeProfile === this.pictureContainers.length) {
      this.activeProfile = 1
    } else {
      this.activeProfile += 1
    }

    this.pictureContainers.forEach(container => container.classList.remove('profile__picture-container--active'))

    this.backgroundImages.forEach(image => {
      if (image.classList.contains(`profile__background-image--profile-${this.activeProfile}`)) {
        image.classList.add(`profile__background-image--active`)
      } else {
        image.classList.remove(`profile__background-image--active`)
      }
    })

    this.pictureContainers[this.activeProfile - 1].classList.add('profile__picture-container--active')
    this.resize()
  }

  resize () {
    const activeContainer = this.element.querySelector('.profile__picture-container--active')

    if (!activeContainer) {
      return
    }

    const informationContainer = activeContainer.querySelector('.profile__information-container')
    const picture = activeContainer.querySelector('.picture')

    if (!informationContainer || !picture) {
      return
    }

    window.requestAnimationFrame(() => {
      const height = `${informationContainer.offsetHeight + parseInt(window.getComputedStyle(picture).marginBottom, 10)}px`

      this.container.style.marginBottom = height

      if (window.matchMedia('(max-width: 799px)').matches) {
        this.button.style.transform = `translateY(${height})`
      } else {
        this.button.style.transform = null
      }
    })
  }

  async rotateWords () {
    if (!this.words.length) {
      return
    }

    const activeWord = this.words.filter(word => word.classList.contains('profile__title-word--visible'))[0]

    if (activeWord) {
      activeWord.classList.remove('profile__title-word--animating-in')
      activeWord.classList.add('profile__title-word--animating-out')
      await sleep(375)
      activeWord.classList.remove('profile__title-word--visible')
      activeWord.classList.remove('profile__title-word--animating-out')
    }

    const nextWord = activeWord ? (this.words[this.words.indexOf(activeWord) + 1] || this.words[0]) : this.words[0]

    nextWord.classList.add('profile__title-word--visible')
    nextWord.classList.add('profile__title-word--animating-in')

    await sleep(WORDS_INTERVAL)

    window.requestAnimationFrame(() => this.rotateWords())
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.profile').forEach(element => {
  element.instance = element.instance || new Profile(element)
}))
