<template>
  <div>
    {{ sequence.join(" ") }}
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
      <img-item
        v-for="card in cards"
        :num="card.key"
        :src="card.src"
        :key="card.key"
      />
      <div class="swiper-scrollbar"></div>
      <div slot="button-prev" class="swiper-button-prev" />
      <div slot="button-next" class="swiper-button-next" />
    </swiper>
  </div>
</template>

<script>
import ImageCard from "@/components/ImageCard.vue";
const {spawnSync,execSync} = require("child_process");

export default {
  name: "EachStep",
  components: {
    "img-item": ImageCard,
  },
  props: ["sequence"],
  data() {
    return {
      cards: [],
      count: 0,
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
  created: function () {
    //console.log("created");
    //this.searchandappend();
  },
  mounted: function () {
    console.log("mounted");
    this.searchandappend();
  },
  beforeUpdate: function () {
    //console.log("Beforepdate");
    //this.searchandappend();
  },
  updated: function () {
    //console.log("update");
    //this.searchandappend();
  },
  methods: {
    searchandappend: function () {
      var dir = this.sequence.join("");
      var path = "$PWD/py/svg/" + dir + "/*";
      // TODO:めちゃくちゃハードコーディンくしちゃってる

      // const stdout = spawnSync('python',["./py/main.py"],{
      //   detached: true,
      //   stdio: 'ignore'
      // })

      //execで書く
      //const stdout = execSync("ls -d1 $PWD" + path);
      //const urls = stdout.toString().split("\n");
      //spawnで書く spawnはストリームで帰ってくる
      const spawn = spawnSync('ls',['-d1',path], { shell: true});
      var urls = spawn.stdout.toString().split("\n");
      urls.pop();
      //console.log(urls);
      for (var item in urls) {
        this.appendSlide(urls[item]);
        //console.log(urls[item]);
      }
    },
    showFileInputDialog: function (event) {
      const { dialog } = require("electron").remote;
      let src = dialog.showOpenDialogSync(null, {
        properties: ["openFile", "multiSelections"],
        title: "Select image files",
        defaultPath: ".",
        filters: [{ name: "image file", extensions: ["svg"] }],
      });
      for (var item in src) {
        this.appendSlide(src[item]);
        console.log(src[item]);
      }
    },
    appendSlide: function (src) {
      if (typeof src != "string") {
        src = "";
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