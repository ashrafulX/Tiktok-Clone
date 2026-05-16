/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./**/*.html",
    "./**/forms.py",
  ],
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',  // or '72px', etc.
      }
    }
  },
  plugins: [],
}
