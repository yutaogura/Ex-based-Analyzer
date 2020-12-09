<template>
  <div>
    {{ sequence.join(" ") }}

    <!-- 任意画像選択と削除ボタン -->
    <!-- <v-btn icon color="green" @click="showFileInputDialog"
      ><v-icon>mdi-folder-multiple-image</v-icon></v-btn
    >
    <v-btn icon color="green" @click="clearSlide"
      ><v-icon>mdi-trash-can</v-icon></v-btn
    > -->
    <v-btn icon color="green" @click="playSound"
      ><v-icon>mdi-volume-high</v-icon></v-btn
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
const Tone = require('tone');
const {spawnSync,execSync} = require("child_process");

const SvgSrcUrl = '/py/svg/';

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
  },
  mounted: function () {
    console.log("mounted");
    this.SearchAppendSlide();
  },
  beforeUpdate: function () {
    //console.log("Beforepdate");
  },
  updated: function () {
    //console.log("update");
  },
  methods: {
    SearchAppendSlide: function () {
      var dir = this.sequence.join("");
      var path = "$PWD/"+ SvgSrcUrl + dir + "/*";

      const spawn = spawnSync('ls',['-d1',path], { shell: true});
      var urls = spawn.stdout.toString().split("\n");
      urls.pop(); //リスト末尾の空白文字を除去
      // console.log(urls);

      for (var item in urls) {
        this.appendSlide(urls[item]);
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
        // console.log(src[item]);
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
    playSound: function(){
      var Dm7 = ['D3', 'F4', 'A4', 'C5', 'E5'];
      var G7 = ['G3', 'F4','A4','B4','D5'];
      var CM7 = ['C3', 'E4', 'G4','B4','D5'];
      var A7 = ['A3', 'Db4','E4','G4', 'A4']
      const sequence =[['0:0:0', Dm7],
                      ['0:1:0', G7],
                      ['0:2:0', CM7],
                      ['0:3:0',A7]];


      var synth = new Tone.PolySynth().toDestination();
      function setplay(time,note){synth.triggerAttackRelease(note,'4n',time);};
      const melody = new Tone.Part(setplay,sequence);
      // melody.stop();
      // melody.start();
      //ループ回数
      melody.loop = 0; 
      //テンポ
      Tone.Transport.bpm.value = 60;
      //再生実行
      Tone.Transport.cancel()
      melody.start();
      Tone.Transport.start(); 
    }
  },
};
</script>

<style>
@import "swiper/css/swiper.css";
</style>