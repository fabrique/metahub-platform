
// Browser update message. Choose the list of browsers via the selection tool at: https://browser-update.org/
// For customization options, see: https://browser-update.org/customize.html
export default function showBrowserUpdateMessage (options = { vs: { i: 10, f: -2, o: -2, s: 9, c: -2 }, api: 4, test: true, insecure: true, unsupported: true }) {
  const showDelay = 5000

  window.$buoop = options

  function insertStyles () {
    let style = ''
    style += 'html { margin-top: 0 !important; }'
    style += '#buorg { width: 60%; top: 0; left: 20%; background: #fff; text-align: center; color: #000; line-height: 155%; border: 0; box-shadow: 0 0 3px rgba(0, 0, 0, .25); }'
    style += '#buorg > div { padding: 10px 20px; }'
    style += '#buorg > div > a:before { content: ""; display: table; }'
    style += '#buorgclose { top: 10px; right: 10px; }'
    style += '#buorg a { color: initial; }'

    const e = document.createElement('style')
    e.id = 'browser-update-styles'
    e.innerText = style
    document.body.appendChild(e)
  }

  function insertScript () {
    const e = document.createElement('script')
    e.id = 'browser-update-script'
    e.src = '//browser-update.org/update.min.js'
    document.body.appendChild(e)
  }

  function initNotice () {
    window.setTimeout(() => {
      insertStyles()
      insertScript()
    }, showDelay)
  }

  try {
    window.addEventListener('DOMContentLoaded', initNotice, false)
  } catch (e) {
    window.attachEvent('onload', initNotice)
  }
}
