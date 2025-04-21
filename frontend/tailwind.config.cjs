/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#0ea5e9',
        secondary: '#10b981',
        custom: {
          50: '#ecfeff',
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      backgroundColor: {
        'page-light': '#f8fafc',
        'page-dark': '#0f172a',
      },
      textColor: {
        'primary-light': '#1e293b',
        'primary-dark': '#f8fafc',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}; 