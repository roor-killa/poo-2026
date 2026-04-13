import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  "#e8f4fd",
          100: "#d1e9fb",
          500: "#2E75B6",
          600: "#1F4E79",
          700: "#163a5a",
        },
      },
    },
  },
  plugins: [],
};

export default config;
