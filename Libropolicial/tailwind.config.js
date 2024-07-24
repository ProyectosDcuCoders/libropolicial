/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Indica las rutas donde Tailwind buscará los archivos HTML
    './templates/**/*.html',
    './**/templates/**/*.html',
    './comisarias/templates/**/*.html',
    './divisioncomunicaciones/templates/**/*.html',
    './divisioncomunicaciones/**/*.html',
    './comisarias/**/*.html',
    './static/**/*.css',  // También puede incluir CSS estático si es necesario
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
