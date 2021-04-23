// Print bootlogo image file to terminal (if it's iTerm)
const { createReadStream } = require('fs')

const showImage = string => console.log(`\n\x1b]1337;File=inline=1;width=auto;height=5;preserveAspectRatio=1:${string}\x07\n`)

async function printBootLogo (filepath = 'sonic/images/bootlogo.png', base64string = 'iVBORw0KGgoAAAANSUhEUgAAANwAAAC5BAMAAACxTUxbAAAAFVBMVEUAAAAZT//+/v+ftv9tj/8uX/9Ldf/Pg2P6AAAAAXRSTlMAQObYZgAABCBJREFUeNrtmst22jAQhq03kMxljwTsLVr20LyAyUn3btP3f4UecMyfIimWPcOU5PjbJORyPv7R6GLsYmJiYmKCGWXeo/kFoUvGaFKwWpAsjYwMaDEbf0CTg5aJBmRsQMvY4JOxwSdjg0/GBh/JJukzRtKnjIgPNkmfGY+MDYiUEmiZcPCJhAMy4YBIOKBlwsEnEg4IhUM82XyFcLsQJp/E4iIZDwEFtyJiPFmfvqmU1M43IC8pXtAB9+2X4N810cffrXyyke1yX50S0QFhnRLRAZHOBEpEB4R1SkQHPqcue2f/sjr1WTcELSiDjl7G397a3d70wGRbeHvB1QSdyeZobY5P89hO9oprenR028JasB5XSzUsHDiM0amB4YAbozP5lPZfvqeHjm5DW/Z2p6aXErUElYnDEm4W6LZJHd2GvgTpWtI3HG8zq6k5wi1h6ZnqtHAYusxq0sJh1oUcmGsJfsV0q3ydMmM7Bbh8naHqwsFbXIpLCAegSA+etzV0pHDLuG518zcrJt08rtveNO8aOlItMe3SvXJsX2tiOOhCbrup4dGVtr9X2tcxneLSVTfDW0V1ZiinhG5zU+8Vgw5r2N4sfWpTKLuZQawldNtgBrqbs8yGU9fg27A1fZeWVku8dReZEw0ak1OHvljEZ8I8qVNjdFghw8MtQjsuHZL46CJdJnWGUbdFM3Hr6ojOoTG5dWjBULfAS9LQoVQueo5Ap1x0NfGgGeosQIXLIF2MIUv0NqprUG3o0uTrNlFdhR9CRxWWmGJR3bxXB1SeropeV64wdFjEqL4S69UytsH6HB3IORpV0TOgaxM73+l0QfEh3SGtm7mmDbiFjuKbQTez4cQ7bnB4oN2yQKQmrjuch7N6Sw0dybd4v34ErXmyNQ5+LLeX07r1uVdNoKPF850uvI7dees63YH6TAl02IsCtt2YNnRdlwnigE2nQ6fQWvOE3TVC9TamDjriPO/VnbCosKxiWDKj113HtqhEGyZe/fHHR76dg0QbWvOQvNJz9fVqUhNtaM0qeaXnujGt2e42lXaNTono5m1K+o20a4scUkO3fvvFmvHRkfObv2RILyqrjFoOOEg7Z5O6EzqFHg5lTOmOeUNH+xQOY+fPX+jhwCntq9uzE+td0OUH8X76i5QxXLjThbOvPxw9Hi7TNSFcVnO63dPrD389AWrGcGE53f7FnHm2dvfUbhjUcGmf+4btyXRoVp15huyPicFTS/C6c9bv9i+1iaKZdWbsPXpl7sHH4T65Tj9ILck6+k1zuk1SJ/IkE0RfVKcf7dFdM5iHeQ7t4Z4TjurG5dbDdZT0xTCdptVbZ+voh5mBHzXQT6JFFtl/S7EBpoezdb5OF5nQbQXKkIGi2grYxvuK+6FkbCC/kPwJi4mJiYmJiYn/wV+vLnD1DCGhfQAAAABJRU5ErkJggg==') {
  if (!process.env.TERM_PROGRAM === 'iTerm.app') {
    return
  }

  if (!filepath && base64string) {
    showImage(base64string)
    return
  }

  const stream = createReadStream(filepath, 'base64')
  let string = ''

  stream.on('data', data => {
    string += data
  })

  stream.on('end', () => showImage(string))
}

module.exports = printBootLogo
