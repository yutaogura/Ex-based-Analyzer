<template>
  <v-app>
    <no-ssr>
      <div class="e-nuxt-container">
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
        <!-- v-forの引数でindexを指定 -->
        <div v-for="(value, index) in sequence" :key="index">
           <!-- メソッドにindexを渡す -->
          <each-step :ref="'childe'+index" :sequence="sequence.slice(0, index + 1)" />
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

export default {
  components: {
    "img-item": ImageCard,
    "each-step": EachStep,
  },
  data() {
    return {
      externalContent: "",
      sequence: [],
      sequence_data: "",
    };
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.$swiper;
    },
  },
  methods: {

    async resetSequence(){
      this.sequence.splice(0);
      console.log(this.sequence);
      return "done"
    }
    ,
    async submitText(event) {
      const { dialog } = require("electron").remote;

      // this.$refs.EachStep.searchandappend();

      // TODO:check vaild chord symbol
      // dialog.showErrorBox("Error", "無効なコードシンボルが含まれています");

      //初期化
      const result = await this.resetSequence();
      console.log(result);

      //target.txtへの書き込み
      var fs = require("fs");
      // 同期で行う場合
      try {
        fs.writeFileSync("py/target.txt", this.sequence_data);
        console.log("target.txt is writed");
      } catch (e) {
        console.log(e);
      }

      //非同期実行
      //const { spawn } = require('child_process')
      //const childProcess = spawn('python', ['./py/main.py'])

      //child processとしてコマンド実行
      const { spawnSync} = require('child_process')
      const stdout = spawnSync('python',["./py/main.py"],{
        detached: true,
        stdio: 'ignore'
      })
      //console.log(`stdout: ${stdout.toString()}`)
      //analyseボタン押下で子のメソッド発火?
      // console.log(this.$refs);
      // for (var step in this.$refs){
      //       console.log(step);
      //       //step.searchandappend();
      // }
      //代入
      this.sequence = this.sequence_data.split(" ");
      console.log(this.sequence);
    },
  },
};
</script>




<style>
.e-nuxt-container {
  padding: 10px;
  min-height: calc(100vh);
  /* background: linear-gradient(to right, #ece9e6, #ffffff); */
  background: #ece9e6;
  font-family: Helvetica, sans-serif;
}

.e-nuxt-content {
  /* display: flex; */
  /* justify-content: space-around; */
  justify-content: center;
  height: 200px;
  /* padding-top: 200px; */
  align-items: flex-start;
  /* flex-wrap: nowrap; */
}
.table {
  width: 100%;
  table-layout: fixed;
}
</style>
