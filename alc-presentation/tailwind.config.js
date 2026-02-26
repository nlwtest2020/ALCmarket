/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand colors from design
        'alc-dark': '#0f1419',
        'alc-navy': '#1a1f2e',
        'alc-purple': '#8b5cf6',
        'alc-magenta': '#bb88ff',
        'alc-cyan': '#7fe5e0',
        'alc-light-blue': '#8dd3f0',
        'alc-accent': '#4dd0e1',
      },
      fontFamily: {
        'sans': ['Inter', 'Helvetica Neue', 'system-ui', 'sans-serif'],
        'heading': ['Inter', 'Helvetica Neue', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-purple-cyan': 'linear-gradient(to right, #8b5cf6, #7fe5e0)',
        'gradient-magenta-cyan': 'linear-gradient(to right, #bb88ff, #7fe5e0)',
      },
    },
  },
  plugins: [],
}
