/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        pitch: {
          bg: '#0B0E11',
          surface: '#12161B',
          surface2: '#181D24',
          line: '#242B33',
          text: '#E7EDF2',
          muted: '#8A96A3',
          green: '#3E9C5C',
          greenBright: '#4FC77A',
          live: '#FF5A36',
          amber: '#F2B84B',
          card: '#E32A2A',
        },
      },
      fontFamily: {
        display: ['"Barlow Condensed"', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      keyframes: {
        pulseDot: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.35 },
        },
      },
      animation: {
        pulseDot: 'pulseDot 1.4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
