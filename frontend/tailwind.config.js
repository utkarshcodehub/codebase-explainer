export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ['"DM Serif Display"', 'serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        ink: '#1a1a2e',
        parchment: '#faf8f5',
        accent: '#e07a5f',
        muted: '#6b7280',
        border: '#e5e2dc',
        surface: '#f0ede8',
      },
    },
  },
  plugins: [],
}
