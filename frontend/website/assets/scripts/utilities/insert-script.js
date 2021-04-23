
// Insert external script with a delay
export default function insertScript (id = '', src = '', callback = () => {}) {
  if (!id || !src || document.getElementById(id)) {
    callback()

    return
  }

  const script = document.createElement('script')
  const timestamp = Math.floor(Date.now() / 1000)

  document.body.appendChild(script)

  script.onload = callback
  script.id = id
  script.setAttribute('data-timestamp', timestamp)
  script.src = src
}
