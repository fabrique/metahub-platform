
import Component from '../../../assets/scripts/modules/component'
import fireCustomEvent from '../../../assets/scripts/utilities/fire-custom-event'

function getCookie (name) {
  const parts = `; ${document.cookie}`.split(`; ${name}=`)
  return parts.length < 2 ? undefined : parts.pop().split(';').shift()
}

function setCookie (name, value, expiryDays, domain = '*', path = '/') {
  const expiryDate = new Date(new Date().setDate(new Date().getDate() + (expiryDays || 365))).toUTCString()
  const cookie = [`${name}=${value}`]

  cookie.push(`expires=${expiryDate}`)
  cookie.push(`path=${path}`)

  if (domain === '*') {
    const domainParts = window.location.hostname.match(/(.*)([.](.+)[.](.+))/i) || []
    domain = (domainParts.length && domainParts[2] && domainParts[3] && domainParts[3] !== '0') ? domainParts[2] : ''
  }

  if (domain) {
    cookie.push(`domain=${domain}`)
  }

  if (window.location.protocol === 'https:') {
    cookie.push(`secure`)
  }

  cookie.push(`samesite=lax`)

  document.cookie = cookie.join(';')
}

let initTimeout

export default class CookieBarComponent extends Component {
  init () {
    this.bar = this.element.querySelector('.cookie-bar__bar')
    this.details = this.element.querySelector('.cookie-bar__details')

    this.checkboxes = [...this.element.querySelectorAll('input[type="checkbox"]')]

    this.buttonAccept = this.element.querySelector('.button--accept')
    this.buttonReject = this.element.querySelector('.button--reject')
    this.buttonSave = this.element.querySelector('.button--save')
    this.buttonAcceptAll = this.element.querySelector('.button--accept-all')
    this.linkDetails = this.element.querySelector('.link--details')
    this.categoryTextItems = [...this.element.querySelectorAll('.cookie-bar__category-text')]

    this.addEventListeners()

    window.clearTimeout(initTimeout)
    initTimeout = window.setTimeout(() => {
      if (!getCookie('cookies-accepted')) {
        this.showBar()
      } else {
        this.setCategories(getCookie('cookies-accepted').trim().split(','))
      }
    }, 500)
  }

  addEventListeners () {
    window.addEventListener('show-cookie-bar', () => this.showBar())
    window.addEventListener('show-cookie-details', () => this.showDetails())
    window.addEventListener('clear-cookie-settings', () => this.deleteSelection())

    this.buttonAccept.addEventListener('click', event => this.onButtonChangeClick(event, 'accept'))
    this.buttonReject.addEventListener('click', event => this.onButtonChangeClick(event, 'reject'))
    this.buttonAcceptAll.addEventListener('click', event => this.onButtonChangeClick(event, 'accept'))

    this.buttonSave.addEventListener('click', event => this.onButtonChangeClick(event))
    this.linkDetails.addEventListener('click', event => this.onLinkDetailsClick(event))

    for (const item of this.categoryTextItems) {
      item.addEventListener('click', event => this.onCategoryTextItemClick(event))
    }
  }

  onButtonChangeClick (event, status) {
    event.preventDefault()

    if (status === 'accept') {
      this.setCategories(this.getAllCategories())
    } else if (status === 'reject') {
      this.setCategories(this.getDefaultCategory())
    }

    this.applySelection()
    this.hideDetails()
    this.hideBar()
  }

  onLinkDetailsClick (event) {
    event.preventDefault()

    this.showDetails()
    this.hideBar()
  }

  applySelection () {
    const categories = this.getSelectedCategories()

    setCookie('cookies-accepted', categories)
    fireCustomEvent('cookies-accepted', categories)

    window.dataLayer = window.dataLayer || []
    window.dataLayer.push({ 'cookies-categories': undefined }) // Reset values
    window.dataLayer.push({ 'cookies-categories': categories, event: 'cookies-accepted' })
  }

  deleteSelection () {
    const categories = this.getDefaultCategory()

    this.setCategories(categories)

    setCookie('cookies-accepted', '', -365)
    fireCustomEvent('cookies-accepted', categories)

    window.dataLayer = window.dataLayer || []
    window.dataLayer.push({ 'cookies-categories': undefined }) // Reset values
    window.dataLayer.push({ 'cookies-categories': categories, event: 'cookies-accepted' })

    window.setTimeout(() => this.showBar(), 100)
  }

  showBar () {
    window.requestAnimationFrame(() => this.bar.classList.add('cookie-bar__bar--visible'))
    this.hideDetails()
  }

  hideBar () {
    window.requestAnimationFrame(() => this.bar.classList.remove('cookie-bar__bar--visible'))
  }

  showDetails () {
    window.requestAnimationFrame(() => this.details.classList.add('cookie-bar__details--visible'))
    this.hideBar()
  }

  hideDetails () {
    window.requestAnimationFrame(() => this.details.classList.remove('cookie-bar__details--visible'))
  }

  getSelectedCategories () {
    return this.checkboxes.filter(checkbox => checkbox.checked).map(checkbox => checkbox.name) || []
  }

  getAllCategories () {
    return this.checkboxes.map(checkbox => checkbox.name) || []
  }

  getDefaultCategory () {
    return this.checkboxes.filter(checkbox => checkbox.disabled).map(checkbox => checkbox.name) || []
  }

  setCategories (categories = []) {
    this.checkboxes.filter(checkbox => !checkbox.disabled).forEach(checkbox => checkbox.checked = false) // eslint-disable-line no-return-assign
    categories.forEach(category => this.checkboxes.filter(checkbox => checkbox.name === category).forEach(checkbox => checkbox.checked = true)) // eslint-disable-line no-return-assign
  }

  onCategoryTextItemClick () {
    const forString = event.target.getAttribute('data-for')

    if (!forString) {
      return
    }

    const target = document.getElementById(forString)

    if (!target) {
      return
    }

    target.click()
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.cookie-bar').forEach(element => {
  element.instance = element.instance || new CookieBarComponent(element)
}))
