
import * as queryString from 'query-string'

import Component from '../../../assets/scripts/modules/component'

class Filters extends Component {
  init () {
    this.search_results_container = document.querySelector('.page-content')
    this.element = this.search_results_container // nasty circumvention of getting a higher level :P
    this.filters = this.element
    this.button = document.querySelector('.filters__button')
    this.filtersContainer = this.element.querySelector('.filters__container')
    this.selectFilters = this.element.querySelectorAll('.filters__dropdown-filter')
    this.dateFilter = this.element.querySelector('.filters__dropdown-date')

    if (!this.button || !this.filtersContainer) {
      return
    }

    this.button.setAttribute('aria-expanded', false)
    this.filtersContainer.setAttribute('aria-hidden', true)

    this.initUI()

    this.initContainerState()
    // this.initDateState()
  }

  initUI () {
    this.button.addEventListener('click', () => this.toggleFiltersContainer())

    this.selectFilters.forEach(filter => {
      const selectId = filter.querySelector('select').id
      filter.addEventListener('filter-selected', (e) => this.updateParams(e, selectId))
      this.initFiltersState(filter)
    })

    this.dateFilter.addEventListener('dates-updated', (e) => this.updateDateParam(e)) // TODO enable this when it is in the data
  }

  updateDateParam (e) {
    const paramId = e.detail.id
    const value = e.detail.value
    const currentUrl = queryString.parse(window.location.search)
    if (e.detail.value === '') {
      delete currentUrl[paramId]
    } else {
      currentUrl[paramId] = value
    }
    const stringifiedUrl = queryString.stringify(currentUrl)
    const updatedUrl = `${window.location.pathname}?${stringifiedUrl}`
    window.history.replaceState('', '', updatedUrl)

    /* eslint-disable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
    const self = this
    fetch(updatedUrl, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(function (response) {
        response.json().then(function (jsondata) {
          self.insertResponseHtml(jsondata.content)
        })
      }).catch(err => {
        // console.log(error.message)
      })
    /* eslint-enable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
  }

  initDateState () {
    // TO DO: Init with min and max as placeholders:
    const parsedQuery = queryString.parse(window.location.search)
    this.dateFilter.querySelectorAll('input').forEach(input => {
      for (var key in parsedQuery) {
        if (key === input.id) {
          input.value = parsedQuery[key]
        }
      }
    })
  }

  updateParams (e, filterId) {
    const currentUrl = queryString.parse(window.location.search)
    currentUrl[filterId] = e.detail
    const stringifiedUrl = queryString.stringify(currentUrl)
    const updatedUrl = `${window.location.pathname}?${stringifiedUrl}`
    window.history.replaceState('', '', updatedUrl)

    /* eslint-disable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
    const self = this
    fetch(updatedUrl, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(function (response) {
        response.json().then(function (jsondata) {
          self.insertResponseHtml(jsondata.content)
        })
      }).catch(err => {
      // console.log(error.message)
      })
  /* eslint-enable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
  }

  initContainerState () {
    this.filtersContainer.style.marginBottom = `-${this.filtersContainer.offsetHeight - 50}px`
    const parsedQuery = queryString.parse(window.location.search)
    delete parsedQuery.search

    // If active filters >= 1 open FiltersContainer:
    if (Object.keys(parsedQuery).length >= 1) {
      this.filtersContainer.style.marginBottom = `0`
      this.filtersContainer.setAttribute('aria-hidden', false)
      this.filtersContainer.classList.add('filters__container--open')
      this.button.setAttribute('aria-expanded', true)
      this.button.querySelector('.button__span').textContent = 'filter ausblenden'
      this.button.querySelector('.button__long-title').textContent = 'filter ausblenden'
    }
  }

  initFiltersState (filter) {
    const selectId = filter.querySelector('select').id
    const parsedQuery = queryString.parse(window.location.search)

    if (selectId in parsedQuery) {
      const selectId = filter.querySelector('select').id
      const filterValue = parsedQuery[selectId]
      const options = filter.querySelectorAll('option')
      const buttonText = filter.querySelector('.select-dropdown-text')
      // Update selected attribute of relevant option:
      for (var i = 0, len = options.length; i < len; i++) {
        if (options[i].value === filterValue) {
          options[i].setAttribute('selected', true)
          // Update buttonText:
          buttonText.textContent = options[i].text
        } else {
          options[i].removeAttribute('selected', true)
        }
      }
    }
  }

  insertResponseHtml (responseHtml) {
    this.search_results_container.innerHTML = responseHtml
    this.init()
    window.dispatchEvent(new CustomEvent('re-init-search-afterfilter'))
    window.dispatchEvent(new CustomEvent('re-init-images'))
  }

  toggleFiltersContainer () {
    if (this.button.getAttribute('aria-expanded') === 'true') {
      this.filtersContainer.setAttribute('aria-hidden', true)
      this.filtersContainer.classList.remove('filters__container--open')
      this.button.setAttribute('aria-expanded', false)
      this.button.querySelector('.button__span').textContent = 'Filter anzeigen'
      this.button.querySelector('.button__long-title').textContent = 'Filter anzeigen'

      this.filtersContainer.style.transition = `transform .3s ease, margin-bottom .3s ease`
      this.filtersContainer.style.marginBottom = `-${this.filtersContainer.offsetHeight - 50}px`
    } else {
      this.filtersContainer.setAttribute('aria-hidden', false)
      this.filtersContainer.classList.add('filters__container--open')
      this.button.setAttribute('aria-expanded', true)
      this.button.querySelector('.button__span').textContent = 'Filter verbergen'
      this.button.querySelector('.button__long-title').textContent = 'Filter verbergen'

      this.filtersContainer.style.transition = `transform .3s ease, margin-bottom .3s ease`
      this.filtersContainer.style.marginBottom = `0`
    }
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.filters').forEach(element => {
  element.instance = element.instance || new Filters(element)
}))

window.addEventListener('re-init-after-filter-disable', () => document.querySelectorAll('.filters').forEach(element => {
  element.instance = element.instance || new Filters(element)
}))
