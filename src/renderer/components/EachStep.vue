<template>
  <div>
    {{sequence.join(' ')}}
    <v-btn icon color="green" @click="showFileInputDialog"
      ><v-icon>mdi-folder-multiple-image</v-icon></v-btn
    >
    <v-btn icon color="green" @click="appendSlide"
      ><v-icon>mdi-plus-circle</v-icon></v-btn
    >
    <v-btn icon color="green" @click="clearSlide"
      ><v-icon>mdi-trash-can</v-icon></v-btn
    >
    <swiper ref="mySwiper" :options="swiperOption">
      <img-item v-for="card in cards" :num="card.key" :src="card.src" :key="card.key" />
      <div class="swiper-scrollbar"></div>
      <div slot="button-prev" class="swiper-button-prev" />
      <div slot="button-next" class="swiper-button-next" />
    </swiper>
  </div>
</template>

<script>
import ImageCard from "@/components/ImageCard.vue";
const fs = require('fs')

export default {
  name: "EachStep",
  components: {
    "img-item": ImageCard,
  },
  props: ["sequence"],
  data() {
    return {
      cards: [],
      count:0,
      swiperOption: {
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        slidesPerView: 3,
        centeredSlides: false,
        spaceBetween: 5,
        loop: false,
        // loopedSlides:6,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
    };
  },
  methods: {
    showFileInputDialog: function (event) {
      const { dialog } = require("electron").remote;
      let src = dialog.showOpenDialogSync(null, {
        properties: ["openFile", "multiSelections"],
        title: "Select image files",
        defaultPath: ".",
        filters: [{ name: "image file", extensions: ["svg"] }],
      });
      for(var item in src){
        this.appendSlide(src[item])
        console.log(src[item])
      } 
    },
    appendSlide: function (src) {
      if(typeof(src) != "string"){
        src = ""
      } 
      this.cards.push({
        key: this.count++,
        src: src,
      });
    },
    clearSlide: function (src) {
      this.cards.splice(0);
      this.count = 0;
    },
  },
};
</script>

<style>
@import "swiper/css/swiper.css";

</style>