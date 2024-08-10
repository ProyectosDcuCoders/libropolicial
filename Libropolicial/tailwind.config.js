// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Usa la clase "dark" para habilitar el modo oscuro
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './comisarias/templates/**/*.html',
    './divisioncomunicaciones/templates/**/*.html',
    './divisioncomunicaciones/**/*.html',
    './comisarias/**/*.html',
    './static/**/*.css',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
