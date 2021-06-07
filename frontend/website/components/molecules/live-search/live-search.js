
import * as queryString from 'query-string'

import Component from '../../../assets/scripts/modules/component'

class LiveSearch extends Component {
  init () {
    this.liveSearch = this.element
    this.inputField = this.element.querySelector('.live-search__input-field')
    this.resultsContainer = this.element.querySelector('.live-search__results')
    this.form = this.element.querySelector('.live-search__form')
    this.live_search_url = this.form.dataset.lsurl
    this.searchUrl = this.form.dataset.surl
    this.searchIcon = this.element.querySelector('.live-search__search-icon')

    this.inputField.addEventListener('keyup', (e) => this.onHandleChange(e))
    // this.inputField.addEventListener('focus', () => this.liveSearch.classList.add('live-search--focused'))
    this.form.addEventListener('submit', (e) => this.onSubmit(e))
    this.searchIcon.addEventListener('click', (e) => this.onSubmit(e))

    this.liveSearch.addEventListener('keydown', event => this.onKeyPress(event))

    this.initSearchField()

    this.isHomepage = this.liveSearch.dataset.id === 'homepage'
  }

  onHandleChange (e) {
    const inputValue = e.target.value
    // const url = `${window.location.origin}${window.location.pathname}${this.live_search_url}/?search=${inputValue}`
    const url = `${this.live_search_url}?search=${inputValue}`

    /* eslint-disable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
    const self = this
    fetch(url).then(function (response) {
      response.json().then(function (jsondata) {
        self.insertResponseHtml(jsondata.content)
      })
    }).catch(err => this.insertResponseHtml('<div>no results found</div>'))
    /* eslint-enable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */

    if (e.target.value.length >= 3) {
      this.liveSearch.classList.add('live-search--active')
      this.liveSearch.classList.add('live-search--focused')
    } else {
      this.liveSearch.classList.remove('live-search--active')
      this.liveSearch.classList.remove('live-search--focused')
    }
  }

  insertResponseHtml (responseHtml) {
    this.resultsContainer.innerHTML = responseHtml
  }

  initSearchField () {
    const parsedQuery = queryString.parse(window.location.search)
    if ('search' in parsedQuery) {
      this.inputField.value = parsedQuery.search
    }
  }

  onSubmit (e) {
    e.preventDefault()
    // console.log('submit')
    const queryParams = queryString.parse(window.location.search)
    if (this.inputField.value === '') {
      delete queryParams.search
    } else {
      queryParams.search = this.inputField.value
    }
    const stringifiedParams = queryString.stringify(queryParams)
    const url = `${this.searchUrl}?${stringifiedParams}`
    window.location.replace(url)
  }

  onKeyPress (event) {
    if (!this.liveSearch.classList.contains('live-search--active')) {
      return
    }

    // Cannot fake with Tab and Shift+Tab, since event.shitKey only has a getter.
    // const activeElement = document.activeElement
    let nextElement

    if (event.keyCode === 40) { // Arrow down
      if (document.activeElement === this.inputField) {
        nextElement = this.resultsContainer.querySelector('.live-search__result-item')
      } else if (document.activeElement === this.resultsContainer.querySelector('.live-search__result-item:last-child')) {
        nextElement = this.inputField
      } else {
        nextElement = document.activeElement.nextElementSibling
      }
    } else if (event.keyCode === 38) { // Arrow up
      if (document.activeElement === this.inputField) {
        nextElement = this.resultsContainer.querySelector('.live-search__result-item:last-child')
      } else if (document.activeElement === this.resultsContainer.querySelector('.live-search__result-item')) {
        nextElement = this.inputField
      } else {
        nextElement = document.activeElement.previousElementSibling
      }
    }

    if (!nextElement) {
      return
    }

    setTimeout(() => nextElement.focus(), 10)
    event.preventDefault()
    event.stopPropagation()
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.live-search').forEach(element => {
  element.instance = element.instance || new LiveSearch(element)
}))
