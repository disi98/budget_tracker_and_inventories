/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './budget/**/*.{html, js}',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
  ],
}

