import { defineConfig, envField } from 'astro/config';
import tailwindcss from '@tailwindcss/vite'
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  vite: {
    plugins: [tailwindcss()],
  },
  adapter: node({
    mode: 'standalone',
  }),
  env: {
    schema: {
      API_URL: envField.string({ context: "server", access: "public", optional: false }),
    }
  }
}); 