// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: [
    '@nuxt/content',
    '@nuxtjs/tailwindcss',
    'shadcn-nuxt',
    '@nuxt/image',
    '@pinia/nuxt'
  ],
  runtimeConfig: {
    public: {
      redlmApiBase: 'http://localhost:8080', // override with `NUXT_PUBLIC_REDLM_API_BASE` in `ui/.env` (see `/ui/.env.sample`)
    }
  },
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  }
})