
// Konami code
// Pass a callback function to execute when the code has been entered
export default function konamiCode (callback) {
  let count = 0

  window.addEventListener('keydown', function (event) {
    const code = '&&((%\'%\'BA'

    count = code[count].charCodeAt(0) === event.keyCode ? count + 1 : 0

    if (count > 9) {
      callback()
    }

    count %= 10
  })
}
