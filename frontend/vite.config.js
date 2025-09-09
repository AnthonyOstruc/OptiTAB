import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: tag => tag === 'math-field'
        }
      }
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    chunkSizeWarningLimit: 5000, // Increase warning limit to 5MB
    rollupOptions: {
      output: {
        manualChunks: {
          // Core framework chunks
          vendor: ['vue', 'vue-router', 'pinia'],

          // UI libraries
          ui: ['@heroicons/vue', 'axios', 'lodash-es'],

          // Math libraries (split for better caching)
          math: ['mathjax'],
          mathlive: ['mathlive'],

          // Heavy libraries
          calculator: ['plotly.js-dist-min'],
          pdf: ['jspdf', 'html2canvas'],

          // Utility libraries
          marked: ['marked']
        }
      }
    }
  },
  // Supprime console.* et debugger uniquement en production
  esbuild: mode === 'production' ? { drop: ['console', 'debugger'] } : undefined,
  define: {
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  }
}))
