// Dart-Sass configuration

const { readFileSync } = require('fs')
const { join } = require('path')

module.exports = function (api) {
  const sass = require('sass')
  const config = require(join(process.cwd(), 'config/sonic'))

  const outputStyle = (api.env === 'production') ? 'compressed' : 'expanded'
  const precision = 2

  const functions = {
    'timestamp()': () => new sass.types.Number(new Date().getTime(), 'ms'),
    'readfile($filepath)': filepath => {
      const realpath = join(process.cwd(), 'website/', filepath.dartValue.text)
      let source = ''

      try {
        source = readFileSync(realpath, 'utf-8')
      } catch (e) {
        console.error(`Sass readfile(): Could not read from '${filepath.dartValue.text}'; resolves to '${realpath}'.`)
      }

      return new sass.types.String(source)
    },
    // These 2 are useful because dart-sass defaults to CSS min() and max() functions
    'math_min($num1, $num2)': (num1, num2) => new sass.types.Number(Math.min(num1, num2)),
    'math_max($num1, $num2)': (num1, num2) => new sass.types.Number(Math.max(num1, num2)),
    'math_floor($num)': num => new sass.types.Number(Math.floor(num)),
    'math_ceil($num)': num => new sass.types.Number(Math.ceil(num)),
    // 'math_round()': () => new sass.types.Number(Math.round())
    'env_development()': () => new sass.types.Boolean(global.buildEnv === 'development')
    // 'env_production()': () => new sass.types.Boolean(global.buildEnv === 'production'),
  }

  return { outputStyle, precision, functions }
}
