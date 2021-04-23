
import * as queryString from 'query-string'

import Component from '../../../assets/scripts/modules/component'

class SearchResults extends Component {
  init () {
    this.search_results_container = document.querySelector('.page-content')

    this.totalResultsValue = this.element.querySelector('.search-results__total-results')
    this.searchTerm = this.element.querySelector('.search-results__results-search-term')
    this.gridContainer = this.element.querySelector('.search-results__grid-container')
    this.filterList = this.element.querySelector('.search-results__results-active-filters')
    this.filtersContainer = this.element.querySelector('.search-results__filters')
    this.filters = this.filtersContainer.querySelectorAll('.dropdown-filter--select')

    // this.fetchResults()
    this.updateActiveFiltersText()

    window.addEventListener('filter-selected', () => this.updateActiveFiltersText())

    this.animateCards()
  }

  animateCards () {
    setTimeout(function () {
      const resultItems = this.element.querySelectorAll('.search-results__results-item')
      resultItems.forEach(item => item.classList.add('search-results__results-item--in-view'))
    }.bind(this), 50)
  }

  fetchResults () {
    const currentQueryString = window.location.search

    if (currentQueryString) {
      const url = `${window.location.pathname}${currentQueryString}`

      /* eslint-disable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
      fetch(url)
        .then(res => {
          if (res.ok) {
            // this.updateInnerHtml(this.gridContainer, res.body.total)
          }
        })
        .catch(error => {
          throw new Error(error)
        })
      /* eslint-enable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
    } else {
      // Render highlights
    }
  }

  updateActiveFiltersText () {
    const parsedQuery = queryString.parse(location.search)
    const activeFilters = []

    // console.log('updatin filters')

    if (this.searchTerm) {
      this.searchTerm.innerText = queryString.parse(location.search).search !== undefined ? `"${queryString.parse(location.search).search}"` : ''
    }

    Object.keys(parsedQuery).forEach((key, i) => {
      if (key.startsWith('id_')) {
        const filterName = key
        let filterValue = parsedQuery[key]

        if (key === 'id_is_highlight') {
          filterValue = 'Highlights'
        } else if (key.startsWith('id_series')) {
          filterValue = 'Objektserie'
        }
        const activeFilterObject = {
          filterName: filterName,
          filterValue: filterValue
        }
        activeFilters.push(activeFilterObject)
      }
    })

    // Render Active Filter buttons:
    if (activeFilters.length >= 1) {
      this.filterList.classList.add('search-results__results-active-filters--active')
    } else {
      this.filterList.classList.remove('search-results__results-active-filters--active')
    }

    this.filterList.innerText = ' gefiltert mit'

    activeFilters.forEach(filter => {
      const button = document.createElement('button')
      button.classList.add('search-results__active-button')
      const span1 = document.createElement('span')
      span1.classList.add('search-results__active-button-title')
      span1.innerText = filter.filterValue // Should insert full name not value
      const span2 = document.createElement('span')
      span2.classList.add('search-results__active-button-close')
      span2.innerText = 'x' // Should be an icon, not text
      button.appendChild(span1)
      button.appendChild(span2)
      button.addEventListener('click', (e) => removeFilter(e, filter.filterName))
      this.filterList.appendChild(button)
    })

    const removeFilter = (e, filterName) => {
      const parsed = queryString.parse(location.search)
      const updatedQuery = { ...parsed }
      delete updatedQuery[filterName]
      const url = `${window.location.pathname}?${queryString.stringify(updatedQuery)}`
      window.history.replaceState('', '', url)

      this.filterList.removeChild(e.target)
      delete parsed.search
      delete parsed[filterName]
      if (Object.keys(parsed).length === 0) {
        this.filterList.classList.remove('search-results__results-active-filters--active')
      }

      /* eslint-disable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
      const self = this
      fetch(url, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      }).then(function (response) {
        response.json().then(function (jsondata) {
          self.insertResponseHtml(jsondata.content)
        })
      }).catch(err => {
        // console.log(error.message)
      })
      /* eslint-enable smells/no-this-assign, handle-callback-err, promise/prefer-await-to-then, promise/always-return, promise/catch-or-return, promise/no-nesting */
    }

    // Brr, this is dirty.. ¯\_(ツ)_/¯
    let resetLink = this.filterList.parentNode.querySelector('.search-results__reset-link')

    if (resetLink) {
      this.resetLink.parentNode.removeChild(resetLink)
    }

    resetLink = document.createElement('a')
    resetLink.classList.add('search-results__reset-link')
    resetLink.href = window.location.href.split(window.location.search)[0]
    resetLink.innerText = 'Filter löschen'
    this.filterList.appendChild(resetLink)
  }

  insertResponseHtml (responseHtml) {
    this.search_results_container.innerHTML = responseHtml
    this.init()
    window.dispatchEvent(new CustomEvent('re-init-search-afterfilter'))
    window.dispatchEvent(new CustomEvent('re-init-images'))
    window.dispatchEvent(new CustomEvent('re-init-after-filter-disable'))
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.search-results').forEach(element => {
  element.instance = element.instance || new SearchResults(element)
}))

window.addEventListener('re-init-search-afterfilter', () => document.querySelectorAll('.search-results').forEach(element => {
  element.instance = element.instance || new SearchResults(element)
}))
