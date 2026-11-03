/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Space Grotesk', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'neo-sm': '2px 2px 0px 0px rgba(15, 23, 42, 1)',
        'neo': '4px 4px 0px 0px rgba(15, 23, 42, 1)',
        'neo-lg': '6px 6px 0px 0px rgba(15, 23, 42, 1)',
        'neo-amber': '4px 4px 0px 0px #F59E0B',
        'neo-blue': '4px 4px 0px 0px #0070BA',
      },
      colors: {
        brand: {
          50: '#F0F7FF',
          100: '#E0EFFF',
          200: '#BAE0FF',
          500: '#0070BA',
          600: '#003087',
          700: '#002266',
          900: '#001438',
        },
        cyber: {
          yellow: '#FFC837',
          amber: '#F5A623',
          orange: '#FF8008',
        }
      }
    },
  },
  plugins: [],
}
