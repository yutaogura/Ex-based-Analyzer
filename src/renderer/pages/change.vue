<template>
  <div class="main_content">
    <h1>Root Graph</h1>
    <p>show the number transition of root expectation</p>
    <v-divider></v-divider>
    <v-text-field
      class="pt-3"
      label="chord sequence"
      :value="input_sequence"
      outlined
      readonly
    >
    </v-text-field>
    <v-layout justify-center>
      <img :src="png_path" class="justify-center " />
    </v-layout>
  </div>
</template>
<script>
import { remote } from "electron";
const fs = require("fs");

export default {
  data() {
    return {
      png_path: "",
      input_sequence: "",
    };
  },
  conputed: {},
  created: function () {
    // 画像のpathが同じ名前になるのでクエリパラメータでタイムスタンプつける必要あり
    var app_path = remote.app.getAppPath() + "/../../";
    this.png_path =
      "file://" +
      app_path +
      "py/linegraph/root.png" +
      "?" +
      new Date().getTime();
    try {
      let target = fs.readFileSync(app_path + "py/target.txt", "utf-8");
      this.input_sequence = target;
    } catch (e) {
      console.log(e);
    }
    // console.log(this.svg_path);
  },
};
</script>
<style>
</style>