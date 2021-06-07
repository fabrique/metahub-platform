// jshint module: true

export function getCookie (name) {
  const parts = `; ${document.cookie}`.split(`; ${name}=`)
  return parts.length < 2 ? undefined : parts.pop().split(';').shift()
}

export function setCookie (name, value, expiryDays, domain = '*', path = '/') {
  const expiryDate = new Date(new Date().setDate(new Date().getDate() + (expiryDays || 365))).toUTCString()
  const cookie = [`${name}=${value}`]

  cookie.push(`Expires=${expiryDate}`)
  cookie.push(`Path=${path}`)

  if (domain === '*') {
    const domainParts = window.location.hostname.match(/(.*)([.](.+)[.](.+))/i) || []
    cookie.push(`Domain=${(domainParts.length && domainParts[2] && domainParts[3] && domainParts[3] !== '0') ? domainParts[2] : ''}`)
  } else {
    cookie.push(`Domain=${location.hostname}`)
  }

  if (window.location.protocol === 'https:') {
    cookie.push(`Secure`)
  }

  cookie.push(`SameSite=Lax`)

  document.cookie = cookie.join('; ').trim()
}
