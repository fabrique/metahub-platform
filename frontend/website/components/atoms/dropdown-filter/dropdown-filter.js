
import Component from '../../../assets/scripts/modules/component'

class DropdownFilter extends Component {
  init () {
    this.filter = this.element

    if (!this.filter) {
      return
    }

    this.select = this.filter.querySelector('.dropdown-filter__select')
    this.dropdownList = this.filter.querySelector('.select-dropdown__list')
    this.listItems = [...this.filter.querySelectorAll('li')]
    this.button = this.filter.querySelector('.select-dropdown__button')
    this.buttonIcon = this.filter.querySelector('.dropdown-filter__button-icon')
    this.inputs = [...this.filter.querySelectorAll('.dropdown-filter__date-input')]
    this.allFilters = [...document.documentElement.querySelectorAll('.select-dropdown__list')]

    this.initSelect()
    this.initDateRange()
  }

  initSelect () {
    if (this.select) { // stil need a native datepicker select solution... this is for mobile dropdowns only (not datepicker)
      this.select.addEventListener('change', () => {
        this.filter.dispatchEvent(new CustomEvent('filter-selected', { detail: this.select.selectedOptions[0].value }))
        window.dispatchEvent(new CustomEvent('filter-selected', { detail: this.select.selectedOptions[0].value }))
      }, false)
    }

    this.listItems.forEach(item => item.addEventListener('click', () => displayUl(item)))

    const displayUl = (element) => {
      if (element.parentNode.classList.contains('select-dropdown__list--date') && (element.tagName === 'LI')) {
        return // if expanded, we need to be able to enter dates...
      }

      const selectDropdown = element.parentNode.getElementsByTagName('ul')
      let elementParentSpan

      // collapse all expanded dropdowns
      this.allFilters.forEach(filter => {
        if (filter !== selectDropdown[0]) {
          filter.classList.remove('select-dropdown__list--active')
        }
      })

      if (element.tagName === 'BUTTON') {
        for (var i = 0, len = selectDropdown.length; i < len; i++) {
          selectDropdown[0].classList.toggle('select-dropdown__list--active')
        }
      } else if (element.tagName === 'LI') {
        // select a dropdown option by clicking, note the datething exception
        elementParentSpan = element.parentNode.parentNode.getElementsByTagName('span')

        element.parentNode.classList.toggle('active')
        // Should only update placeholder fo Select elements:
        if (this.dropdownList.classList.contains('select-dropdown__list--select')) {
          var selectId = element.parentNode.parentNode.parentNode.getElementsByTagName('select')[0]
          selectElement(selectId.id, element.getAttribute('data-value'))
          elementParentSpan[0].textContent = element.textContent
          elementParentSpan[0].parentNode.setAttribute('data-value', element.getAttribute('data-value'))
        }
      }

      if (this.dropdownList.classList.contains('select-dropdown__list--active')) {
        this.buttonIcon.classList.add('dropdown-filter__button-icon--active')
        this.button.classList.add('select-dropdown__button--active')
      } else {
        this.buttonIcon.classList.remove('dropdown-filter__button-icon--active')
        this.button.classList.remove('select-dropdown__button--active')
      }
    }
    const selectElement = (id, valueToSelect) => {
      var element = document.getElementById(id)
      var options = this.filter.querySelectorAll('option')

      element.value = valueToSelect
      element.setAttribute('selected', 'selected')

      for (var i = 0, len = options.length; i < len; i++) {
        if (options[i].value === valueToSelect) {
          options[i].setAttribute('selected', true)
          this.filter.dispatchEvent(new CustomEvent('filter-selected', { detail: options[i].value }))
          window.dispatchEvent(new CustomEvent('filter-selected'))
        } else {
          options[i].removeAttribute('selected', true)
        }
      }
      if (this.dropdownList.classList.contains('select-dropdown__list--select')) {
        this.dropdownList.classList.remove('select-dropdown__list--active')
      }
    }

    var buttonSelect = this.filter.querySelector('.select-dropdown__button')
    buttonSelect.addEventListener('click', () => displayUl(buttonSelect))
  }

  initDateRange () {
    this.inputs.forEach(input => {
      input.addEventListener('keyup', (e) => {
        if (e.target.value.length >= 4) {
          this.filter.dispatchEvent(new CustomEvent('dates-updated', { detail: { id: input.id, value: e.target.value } }))
        }
      })
    })
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.dropdown-filter').forEach(element => {
  element.instance = element.instance || new DropdownFilter(element)
}))

window.addEventListener('re-init-search-afterfilter', () => document.querySelectorAll('.dropdown-filter').forEach(element => {
  element.instance = element.instance || new DropdownFilter(element)
}))
