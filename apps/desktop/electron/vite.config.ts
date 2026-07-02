import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({ root: 'renderer', plugins: [vue()], server: { host: '127.0.0.1', port: 5173 }, build: { outDir: '../dist/renderer', emptyOutDir: true } })
