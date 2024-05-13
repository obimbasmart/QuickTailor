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
        "pc-teal-normal": "#006060"
      },

      fontFamily: {
        "playfair-display": ["Playfair Display", "serif"],
        "roboto": ["Roboto", "serif"],
        "montserrat": ["Montserrat", "sans-serif"],
        "montserrat-alternates": ["Montserrat Alternates", "sans-serif"],
        "obitron": ["Orbitron", "sans-serif"]
      },

    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

