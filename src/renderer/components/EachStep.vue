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
        :rank="card.rank"
        :prob="card.prob"
        :src="card.src"
        :id="card.id"
        :key="card.id"
      />
      <!--  when using v-for with a component, a key is now required -->
      <div class="swiper-scrollbar"></div>
      <div slot="button-prev" class="swiper-button-prev" />
      <div slot="button-next" class="swiper-button-next" />
    </swiper>
  </div>
</template>

<script>
import ImageCard from "@/components/ImageCard.vue";
import chord from "@/const.js"; //定数を別ファイルにやる方法
const fs = require("fs");
import parse_csv from 'csv-parse/lib/sync';

const chordname_regexp = /^([ABCDEFG][b]*)(|7|M7|m7|m|m6|aug|aug7|hdim7|o|o7|sus|sus4)$/;
const root_name = {
  A: 9,
  B: 11,
  C: 0,
  D: 2,
  E: 4,
  F: 5,
  G: 7,
  "A#": 10,
  "B#": 0,
  "C#": 1,
  "D#": 3,
  "E#": 5,
  "F#": 6,
  "G#": 8,
  Ab: 8,
  Bb: 10,
  Cb: 11,
  Db: 1,
  Eb: 3,
  Fb: 4,
  Gb: 6,
};
const type_name = { M7: 0, m7: 1, 7: 2, hdim7: 3, o7: 4 };
const Tone = require("tone");
const { spawnSync, execSync } = require("child_process");

const SvgSrcDir = "py/svg/";
const TempDir = "py/temp/";

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
  computed:{
    step_num_2d : function(){
      var step_num = this.sequence.length - 1;
      var dd = ("00" + step_num).slice(-2);
      return dd
    },
    prob_data : function(){
      var data = []
      try {
        let target = fs.readFileSync("./"+TempDir+this.step_num_2d+"prob.csv",'utf-8');
        data = parse_csv(target)
        // console.log(data);
      } catch (e) {
        console.log(e);
      }
      return data
    },
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
      var path = "$PWD/" + SvgSrcDir + this.step_num_2d + "/*";
      const spawn = spawnSync("ls", ["-d1", path], { shell: true });
      var urls = spawn.stdout.toString().split("\n");
      urls.pop(); //リスト末尾の空白文字を除去
      // console.log(urls);

      for (var item in urls) {
        this.appendSlide(urls[item]);
      }
    },
    // 自分で選ぶやつ
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
      var rank = this.count;
      this.count  = this.count + 1;
      var identification = this.sequence.join() + rank;
      // console.log(identification)
      this.cards.push({
        rank: rank,
        prob: this.prob_data[rank][1],
        id:identification,
        src: src,
      });
    },
    clearSlide: function (src) {
      this.cards.splice(0);
      this.count = 0;
    },
    judge_root: function (symbol) {
      //TODO: 文字列からルートとコードタイプを抜き出して適切なroot_num,chord_type_numを割り当てる
      var match = symbol.match(chordname_regexp);
      var root_num = root_name[match[1]];
      console.log("root_num", root_num);
      return root_num;
    },
    judge_type: function (symbol) {
      var match = symbol.match(chordname_regexp);
      var type_num = type_name[match[2]];
      console.log("type_num", type_num);
      return type_num;
    },
    returnMidiSequence: function (sequence) {
      var play_sequence = [];
      var measure = 0;
      var bar = 0;
      var tick = 0;
      for (var i = 0; i < sequence.length; i++) {
        console.log(sequence[i]);

        var chord_root_num = this.judge_root(sequence[i]);
        var chord_type_num = this.judge_type(sequence[i]);

        var root_note_name3 = [
          "C3",
          "C#3",
          "D3",
          "D#3",
          "E3",
          "F3",
          "F#3",
          "G3",
          "G#3",
          "A3",
          "A#3",
          "B3",
        ];
        var maj_array = [0, 4, 7, 11];
        var min_array = [0, 3, 7, 10];
        var dom_array = [0, 4, 7, 10];
        var hdim_array = [0, 3, 6, 10];
        var dim7_array = [0, 3, 6, 9];
        var minMaj7_array = [0, 3, 7, 11];
        var aug7_array = [0, 4, 8, 11];

        // TODO :　対応表作る
        var chord_type = [
          maj_array,
          min_array,
          dom_array,
          hdim_array,
          dim7_array,
          minMaj7_array,
          aug7_array,
        ];
        var tone_array = Tone.Frequency(
          root_note_name3[chord_root_num]
        ).harmonize(chord_type[chord_type_num]);

        var time_record = measure + ":" + bar + ":" + tick; //0:0:0
        console.log(time_record);
        play_sequence.push([time_record, tone_array]);
        if (bar != 3) {
          bar++;
        } else {
          bar = 0;
          measure++;
        }
      }
      console.log(play_sequence);
      return play_sequence;
    },
    playSound: function () {
      var play_sequence = this.returnMidiSequence(this.sequence);

      var synth = new Tone.PolySynth().toDestination();
      function setplay(time, note) {
        synth.triggerAttackRelease(note, "8n", time);
      }
      const melody = new Tone.Part(setplay, play_sequence);
      // melody.stop();
      // melody.start();
      //ループ回数
      melody.loop = 0;
      //テンポ
      Tone.Transport.bpm.value = 60;
      //再生実行
      Tone.Transport.cancel();
      melody.start();
      Tone.Transport.start();
    },
  },
};
</script>

<style>
@import "swiper/css/swiper.css";
</style>