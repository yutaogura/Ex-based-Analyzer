<template>
  <v-app>
    <no-ssr>
      <div id="demo" :class="[{ collapsed: collapsed }]">
        <div class="demo">
          <sidebar-menu
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
          />
          <div class="e-nuxt-container">
            <!-- <v-icon x-large color="blue darken-2"> mdi-message-text </v-icon> -->
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
            <router-view />
          </div>
        </div>
      </div>
    </no-ssr>
  </v-app>
</template>

<script>
import { remote } from "electron";
import SystemInformation from "@/components/SystemInformation.vue";
import ImageCard from "@/components/ImageCard.vue";
import EachStep from "@/components/EachStep.vue";
import "@/assets/css/loading.css";
import { mdiMidiPort } from "@mdi/js";

const { spawnSync, spawn } = require("child_process");
const util = require("util");
const childProcess = require("child_process");
const exec = util.promisify(childProcess.exec);
const chordname_regexp = /^[ABCDEFG][b]*(|7|M7|m7|m|m6|aug|aug7|hdim7|dim|dim7|sus|sus4)$/;
const fs = require("fs");

export default {
  components: {
    "img-item": ImageCard,
    "each-step": EachStep,
  },
  data() {
    return {
      menu: [
        {
          header: true,
          title: "Ex-based Chord Sequence Analyzer",
          hiddenOnCollapse: true,
        },
        {
          href: "/",
          title: "Tree analysis",
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "tree",
            },
          },
        },
        {
          //href: "/installtaion",
          title: "Change Probability",
          disabled: false,
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "sliders-h",
            },
          },
        },
        {
          //href: "/installtion",
          title: "Check Grammar",
          disabled: true,
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "spell-check",
            },
          },
        },
        {
          //href: "/",
          title: "Settings",
          disabled: true,
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "cogs",
            },
          },
        },
        {
          header: true,
          title: "Others",
          hiddenOnCollapse: true,
        },
        {
          //href: "/",
          title: "Connect MIDI Keyboard",
          disabled: false,
          icon: {
            element: "v-icon",
            class: ["white--text"], 
            text: mdiMidiPort,
          },
        },
        // {
        //   href: "/",
        //   title: "Dropdown Page",
        //   icon: "list-ul",
        //   child: [
        //     {
        //       href: "/",
        //       title: "Sub Page 01",
        //       //icon: "fa fa-file-alt"
        //     },
        //     {
        //       href: "/",
        //       title: "Sub Page 02",
        //       //icon: "fa fa-file-alt"
        //     },
        //   ],
        // },
      ],
      collapsed: true,
      show: false,
      externalContent: "",
      sequence: [],
      sequence_data: "",
      loading: false,
    };
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.$swiper;
    },
  },
  methods: {
    onItemClick(e, i) {
      console.log("onItemClick");
    },
    onCollapse(c) {
      console.log("onCollapse");
      this.collapsed = c;
    },
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
        fs.writeFileSync("py/target.txt", this.sequence_data);
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

#demo {
  padding-left: 350px;
  transition: 0.3s ease;
}
#demo.collapsed {
  padding-left: 50px;
}
/* .demo {
  padding: 10px;
} */
.e-nuxt-container {
  padding: 10px;
  min-height: calc(100vh);
  /* background: linear-gradient(to right, #ece9e6, #ffffff); */
  background: #ece9e6;
  font-family: Helvetica, sans-serif;
  /* max-width: 900px; */
}

.sidebar-overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background-color: #000;
  opacity: 0.5;
  z-index: 900;
}

.table {
  width: 100%;
  table-layout: fixed;
}

.v-icon__svg{
  font-size: 40px;
}

.v-icon__svg{ 
  width: 30px;
  height:30px;
  }

</style>
