/**
 * By default, Nuxt.js is configured to cover most use cases.
 * This default configuration can be overwritten in this file
 * @link {https://nuxtjs.org/guide/configuration/}
 */


module.exports = {
  head: {
    title: 'Ex-based Chord Sequence Analyzer',
    meta: [{ charset: "utf-8" }]
  },
  loading: false,
  plugins: [
    { src: '@/plugins/icons.js' },
    { src: '@/plugins/swiper.js', mode:'client' },
    { src: '@/plugins/sidebar.js', mode:'client' }
  ],
  css:['vue-sidebar-menu/dist/vue-sidebar-menu.css'],
  buildModules: [

  ],
  modules: [
    '@nuxtjs/vuetify',
  ],
  vuetify: {
    theme: {
      themes: {
        light: {
          primary: '#1867c0',
          secondary: '#b0bec5',
          accent: '#8c9eff',
          error: '#b71c1c',
        },
      },
    }
  },
};
