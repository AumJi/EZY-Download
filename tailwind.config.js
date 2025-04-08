/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{astro,html,svelte,vue,js,ts,jsx,tsx}'],
    plugins: [require('daisyui')],
    daisyui: {
      themes : ['bumblebee','sunset']
    }
  }