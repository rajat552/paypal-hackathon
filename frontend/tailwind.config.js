/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef2ff',
          500: '#0070ba',
          600: '#003087',
          900: '#001c48',
        }
      }
    },
  },
  plugins: [],
}
