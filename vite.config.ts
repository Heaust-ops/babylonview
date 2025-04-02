import { defineConfig } from "vite";

export default defineConfig({
  root: "src", // Set project root to 'src'
  build: {
    rollupOptions: {
      input: "src/index.html", // Tell Vite to use index.html from src
    },
  },
});
