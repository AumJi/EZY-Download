/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./frontend/templates/index.html",
              "./static/js/**/*.js"],
    plugins: [require('daisyui')],
    daisyui: {
      themes : ['bumblebee','sunset']
    }
  }