// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    layoutTransition: { name: 'layout', mode: 'out-in' },
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      charset: 'utf-16',
      viewport: 'width=500, initial-scale=1',
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono&display=swap' },
      ]
    }
  },
  runtimeConfig: {
    baseUrl: "http://127.0.0.1:8000",
    public: {
      defaultTemperature: "1",
      defaultTop_k: "4",
      defaultTop_p: "1",
      defaultMax_length: "2140",
      defaultHistory_length: "10",
      defaultSearchTop_k: "6"
    },
  },
  modules: [
    "@nuxtjs/color-mode",
    "@nuxtjs/i18n",
    "@nuxtjs/tailwindcss",
    "@pinia/nuxt",
    "nuxt-icon",
  ],
  css: ["highlight.js/styles/dark.css"],
  i18n: {
    locales: [
      {
        code: "zh",
        iso: "zh-CN",
        file: "zh.json",
        name: "简体中文",
      },
      {
        code: "en",
        iso: "en-US",
        file: "en.json",
        name: "English (US)",
      },
      {
        code: "ja",
        iso: "ja-JP",
        file: "ja.json",
        name: "日本語",
      },
    ],
    langDir: "locales",
    defaultLocale: "en",
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      redirectOn: "root",
    },
    precompile: {
      strictMessage: false,
    },
  },
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.postcss',
    config: {
      darkMode: "class",
      content: [],
      plugins: [require("@tailwindcss/typography")],
    },
  },
  colorMode: {
    classSuffix: "",
  },
  ssr: false,
  devtools: { enabled: false },
});
