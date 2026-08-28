/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        f1: {
          red: '#E10600',
          darkRed: '#B00400',
          carbon: '#10141E',
          card: '#161B26',
          border: '#2A303F',
          muted: '#8B949E',
        },
        compound: {
          soft: '#FF1801',
          medium: '#FFD800',
          hard: '#FFFFFF',
          intermediate: '#39B54A',
          wet: '#00A3E0',
          unknown: '#9CA3AF',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
}
