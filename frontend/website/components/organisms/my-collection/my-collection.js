
import Component from '../../../assets/scripts/modules/component'

export default class MyCollection extends Component {
  init () {
    this.favorites = localStorage.getItem('favorites') || '{}'
    this.getFavorites()
  }

  getFavorites () {
    const url = `${window.location}get_favourites?data=${JSON.stringify(this.favorites)}`

    /* eslint-disable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
    const self = this
    fetch(url, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      }
    }).then(function (response) {
      if (response.ok) {
        response.json().then(function (jsondata) {
          self.updateHtml(jsondata)
          window.dispatchEvent(new CustomEvent('re-init-images'))
        })
      }
    }).catch(error => self.updateHtml([], error))
    /* eslint-enable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
  }

  updateHtml (data, error) {
    const mobileContainers = document.querySelectorAll('.my-collection__grid-column-mobile')
    const tabletContainers = document.querySelectorAll('.my-collection__grid-column-tablet')
    const desktopContainers = document.querySelectorAll('.my-collection__grid-column')

    if (error) {
      const errorContainer = document.querySelector('.my-collection__error')
      errorContainer.innerHTML = '<h2 class="my-collection__subtitle">Unfortunately, something went wrong.</h2>'
      return
    }

    if (data.length === 0) {
      const errorContainer = document.querySelector('.my-collection__error')
      errorContainer.innerHTML = '<h2 class="my-collection__subtitle">You do not have any favourites yet.</h2>'
      return
    }

    for (let i = 0; i < data.length; i++) {
      mobileContainers[0].innerHTML += `<li class="my-collection__results-item">${data[i]}</li>`

      // Tablet
      if (i % 2 === 0) {
        tabletContainers[0].innerHTML += `<li class="my-collection__results-item">${data[i]}</li>`
      } else {
        tabletContainers[1].innerHTML += `<li class="my-collection__results-item">${data[i]}</li>`
      }

      // Desktop
      if (i % 3 === 0) {
        desktopContainers[0].innerHTML += `<li class="my-collection__results-item">${data[i]}</li>`
      } else if (i % 3 === 2) {
        desktopContainers[1].innerHTML += `<li class="my-collection__results-item">${data[i]}</li>`
      } else {
        desktopContainers[2].innerHTML += `<li class="my-collection__results-item">${data[i]}</li>`
      }
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.my-collection').forEach(element => {
  element.instance = element.instance || new MyCollection(element)
}))
