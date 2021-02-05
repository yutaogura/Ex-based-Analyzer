<template>
  <div class="main_content">
    <h1>Root Graph</h1>
    <p>show the number transition of root expectation</p>
    <v-divider></v-divider>
    <v-layout justify-center >
      <img :src="png_path" class="justify-center pt-3" />
    </v-layout>
  </div>
</template>
<script>
import { remote } from "electron";

export default {
  data() {
    return {
      png_path: "",
    };
  },
  created: function () {
    // 画像のpathが同じ名前になるのでクエリパラメータでタイムスタンプつける必要あり
    var app_path = remote.app.getAppPath();
    this.png_path =
      "file://" +
      app_path +
      "../../../py/linegraph/root.png" +
      "?" +
      new Date().getTime();
    // console.log(this.svg_path);
  },
};
</script>
<style>
</style>