import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  plugins: [react()],
  root: 'src',
  base: '/static/',
  build: {
    outDir: path.resolve(__dirname, '../backend/frontend_dist'),
    emptyOutDir: true,
  },
});
