
import Component from '../../../assets/scripts/modules/component'

export default class ArticleDetail extends Component {
  init () {
    this.favoriteButton = this.element.querySelector('.article-detail__icon-favorite')

    this.objectId = this.element.getAttribute('data-id')
    this.category = this.element.getAttribute('data-category')
    const isFavorited = this.isFavorited()

    if (this.favoriteButton) {
      this.favoriteButton.addEventListener('click', () => this.onToggleFavorite())

      if (isFavorited) {
        this.favoriteButton.classList.add('article-detail__icon-favorite--active')
      }
    } else {
      return
    }

    // Toggle this too if the desktop version was favourited
    window.addEventListener('toggle-favorited-desktop', () => {
      // console.log('desktop was (un)favorited')
      if (this.isFavorited()) {
        this.favoriteButton.classList.remove('article-detail__icon-favorite--active')
      } else {
        this.favoriteButton.classList.add('article-detail__icon-favorite--active')
      }
    })
  }

  isFavorited () {
    const favorites = JSON.parse(localStorage.getItem('favorites')) || {}

    if (favorites[this.category]) {
      const index = favorites[this.category].indexOf(this.objectId)
      return index !== -1
    }
    return false
  }

  onToggleFavorite () {
    // This favourite button is only shown on the mobile variant
    // The desktop variant is container in detail-image.js
    // console.log('toggle-fav')
    // console.log(this.category)

    const favorites = JSON.parse(localStorage.getItem('favorites')) || {}

    let index = -1
    if (favorites[this.category]) {
      index = favorites[this.category].indexOf(this.objectId)
      // console.log('category existed')
    } else {
      favorites[this.category] = []
      // console.log('making category')
    }

    if (index === -1) {
      // console.log('add')
      favorites[this.category].push(this.objectId)
      // console.log(favorites)
      localStorage.setItem('favorites', JSON.stringify(favorites))

      this.favoriteButton.classList.add('article-detail__icon-favorite--active')
      window.dispatchEvent(new CustomEvent('toggle-favorited-mobile'))
    } else {
      // console.log('remove')
      favorites[this.category].splice(favorites[this.category].indexOf(this.objectId), 1)
      localStorage.setItem('favorites', JSON.stringify(favorites))

      // Somehow this stays on?
      // console.log(this.favoriteButton.classList)
      this.favoriteButton.classList.remove('article-detail__icon-favorite--active')
      // console.log('call remove')
      this.favoriteButton.classList.remove('button-favorite--active')
      // console.log(this.favoriteButton.classList)
      window.dispatchEvent(new CustomEvent('toggle-favorited-mobile'))
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.article-detail').forEach(element => {
  element.instance = element.instance || new ArticleDetail(element)
}))
