import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve, extname, join } from 'path'
import { existsSync, statSync, createReadStream } from 'fs'

// Ressources gratuites en développement : sert les pages statiques générées par
// « npm run ressources:local » (dossier .ressources-local), comme l'hébergeur
// le fait en ligne avec le dossier dist.
function ressourcesLocales() {
  const dossier = resolve(__dirname, '.ressources-local')
  const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.json': 'application/json', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8', '.md': 'text/markdown; charset=utf-8' }
  return {
    name: 'ressources-locales',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const chemin = decodeURIComponent((req.url || '').split('?')[0])
        if (!/^\/(ressources-gratuites\/|blog\/|llms\.txt$|sitemap-ressources\.xml$)/.test(chemin)) return next()
        const fichier = join(dossier, chemin.endsWith('/') ? `${chemin}index.html` : chemin)
        if (!existsSync(fichier) || !statSync(fichier).isFile()) return next()
        res.setHeader('Content-Type', types[extname(fichier)] || 'application/octet-stream')
        createReadStream(fichier).pipe(res)
      })
    }
  }
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: tag => tag === 'math-field'
        }
      }
    }),
    ressourcesLocales()
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    open: true,
    historyApiFallback: true,
    // Pages générées des ressources gratuites : servies telles quelles, pas surveillées.
    watch: { ignored: ['**/.ressources-local/**'] },
    proxy: {
      '/api': {
        // Par défaut en dev, on cible le backend local.
        // Pour utiliser le backend distant en dev, exportez VITE_USE_REMOTE_IN_DEV=true
        target: process.env.VITE_USE_REMOTE_IN_DEV === 'true'
          ? (process.env.VITE_API_URL || 'https://optitab-backend.onrender.com')
          : 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        timeout: 900000,
        proxyTimeout: 900000,
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
  preview: {
    historyApiFallback: true
  },
  // Supprime console.* et debugger uniquement en production
  esbuild: mode === 'production' ? { drop: ['console', 'debugger'] } : undefined,
  // Minify agressif en production
  define: {
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  }
}))
