import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    build: {
        mode: 'production',
        // mode: 'development',
        rollupOptions: {
            output: {
                chunkFileNames: 'index-[hash].js',
                entryFileNames: 'index.js',
                assetFileNames: 'style.[ext]'
            }
        }
    }, resolve: {
        alias: {
            'vue': 'vue/dist/vue.esm-bundler',
        }
    }
})