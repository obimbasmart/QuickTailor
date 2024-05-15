/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "app/templates/**/*.html",
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        "pc-teal-normal": "#006060",
        "sc-gray-normal": "#F2F2F2",
        "sc-gray-dark": "#606060",
        "sc-gray-light-active": "#D8D8D8",
        "sc-gray-light": "#D8D8D8",
        "blue-500": "#006060",
        "sc-gray-darker": "#2D2D2D"
      },

      fontFamily: {
        "playfair-display": ["Playfair Display", "serif"],
        "roboto": ["Roboto", "serif"],
        "montserrat": ["Montserrat", "sans-serif"],
        "montserrat-alternates": ["Montserrat Alternates", "sans-serif"],
        "obitron": ["Orbitron", "sans-serif"]
      },

      borderWidth: {
        "1": "1px"
      },
      screens: {
        'tablet': '412',
        // => @media (min-width: 580px) { ... }

      }  

    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

