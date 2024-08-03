/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',  // Agrega esta línea
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
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      'xs': {'min': '440px', 'max': '640px'}, // Breakpoint personalizado
    },
    extend: {},
  },
  plugins: [],
}
