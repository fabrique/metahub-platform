
// Insert external script with a delay
export default function insertStylesheet (id = '', href = '', callback = () => {}) {
  if (!id || !href || document.getElementById(id)) {
    callback()

    return
  }

  const link = document.createElement('link')
  const timestamp = Math.floor(Date.now() / 1000)

  document.body.appendChild(link)

  link.onload = callback
  link.id = id
  link.setAttribute('data-timestamp', timestamp)
  link.rel = 'stylesheet'
  link.href = href
}
