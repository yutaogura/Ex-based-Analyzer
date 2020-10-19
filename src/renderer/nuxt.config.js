/**
 * By default, Nuxt.js is configured to cover most use cases.
 * This default configuration can be overwritten in this file
 * @link {https://nuxtjs.org/guide/configuration/}
 */


module.exports = {
  head: {
    title: 'pcfg-app',
    meta: [{ charset: "utf-8" }]
  },
  loading: false,
  plugins: [
    { ssr: true, src: '@/plugins/icons.js' },
    { ssr: false, src: '@/plugins/swiper.js' }
  ],
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
  build: {
    extend: (config) => {
      const svgRule = config.module.rules.find(rule => rule.test.test('.svg'));

      svgRule.test = /\.(png|jpe?g|gif|webp)$/;

      config.module.rules.push({
        test: /\.svg$/,
        loader: 'vue-svg-loader',
      });
    },
  },
};
