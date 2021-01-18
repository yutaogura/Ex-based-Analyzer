<template>
  <v-app>
    <client-only>
        <div class="main_content">
          <!-- <v-icon x-large color="blue darken-2"> mdi-message-text </v-icon> -->
          <h1>Incremental Tree Analysis</h1>
          <v-text-field
            label="chord sequence"
            v-model="sequence_data"
            v-on:keyup.enter="submitText"
            outlined
            clearable
          >
            <template v-slot:append-outer>
              <v-btn color="primary" @click="submitText">Analyse</v-btn>
            </template>
          </v-text-field>
          <div class="loader" v-show="show">Loading...</div>
          <!-- v-forの引数でindexを指定 -->
          <div v-for="(value, index) in sequence" :key="index">
            <!-- メソッドにindexを渡す -->
            <each-step
              :ref="'childe' + index"
              :sequence="sequence.slice(0, index + 1)"
            />
          </div>
          <div></div>
        </div>
        <!-- <sidebar-menu
            class="sidebar"
            :menu="menu"
            :collapsed="collapsed"
            @item-click="onItemClick"
            @toggle-collapse="onCollapse"
          >
            <span slot="toggle-icon"
              ><font-awesome-icon icon="arrows-alt-h"
            /></span>
            <span slot="dropdown-icon">dropdown-icon</span>
          </sidebar-menu>
          <div
            v-if="!collapsed"
            class="sidebar-overlay"
            @click="collapsed = true"
          /> -->
    </client-only>
  </v-app>
</template>

<script>
import { remote } from "electron";
import SystemInformation from "@/components/SystemInformation.vue";
import ImageCard from "@/components/ImageCard.vue";
import EachStep from "@/components/EachStep.vue";
import "@/assets/css/loading.css";

const { spawnSync, spawn } = require("child_process");
const util = require("util");
const childProcess = require("child_process");
const exec = util.promisify(childProcess.exec);
const chordname_regexp = /^[ABCDEFG][b]*(|7|M7|M|m7|m|m6|aug|aug7|hdim7|o|o7|sus|sus4)$/;
const fs = require("fs");
const TARGET_FILE = "py/target.txt";

export default {
  components: {
    "img-item": ImageCard,
    "each-step": EachStep,
  },
  data() {
    return {
      show: false,
      externalContent: "",
      sequence: [],
      sequence_data: "",
      loading: false,
    };
  },
  created() {
    console.log('----- created -----')
    try {
        let target = fs.readFileSync(TARGET_FILE,'utf-8');
        console.log(target);
        this.sequence_data = target;
        this.sequence = target.split(" ");
      } catch (e) {
        console.log(e);
      }
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.$swiper;
    },
  },
  methods: {
    checkCharacter(str) {
      if (str.match(chordname_regexp) == null) {
        return false;
      } else {
        //console.log(str.match(chordname_regexp));
        return true;
      }
    },
    async resetSequence() {
      this.sequence.splice(0);
      console.log(this.sequence);
      return "done";
    },
    async makeSVG() {
      const p = new Promise((resolve, reject) => {
        const stdout = spawn("python", ["./py/main.py"], {
          detached: true,
          stdio: "ignore",
        });
      });
      return p;
    },
    async submitText(event) {
      const { dialog } = require("electron").remote;
      var sep_sequence = this.sequence_data.split(" ");

      for (var symbol in sep_sequence) {
        if (!this.checkCharacter(sep_sequence[symbol])) {
          dialog.showErrorBox("Error", "無効なコードシンボルが含まれています");
          return;
        }
      }

      //初期化
      this.show = true;
      const result = await this.resetSequence();
      console.log(result);

      //target.txtへの書き込み
      try {
        fs.writeFileSync(TARGET_FILE, this.sequence_data);
        console.log("target.txt is writed");
      } catch (e) {
        console.log(e);
      }

      //child processとしてコマンド実行
      await exec("python ./py/main.py", { maxBuffer: 1024 * 1024 });

      //代入
      this.sequence = this.sequence_data.split(" ");
      console.log(this.sequence);
      this.show = false;
    },
  },
};
</script>




<style>
/* idは#　 (１ページに1つだけ)
   class は. (１ページに何度でも)
*/

body,
html {
  margin: 0;
  padding: 0;
}

.main_content {
  padding: 10px;
  min-height: calc(100vh);
  /* background: linear-gradient(to right, #ece9e6, #ffffff); */
  font-family: Helvetica, sans-serif;
  background: #ece9e6;
  /* max-width: 900px; */
}

.table {
  width: 100%;
  table-layout: fixed;
}
</style>
