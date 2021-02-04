<template>
  <swiper-slide>
    <v-container >
    <v-row>
    <v-col>   
    <v-card>
      <!-- <v-card-text>tree {{ num }} {{src}} prob:NaN </v-card-text> -->
      <v-card-text>{{ rank }} : {{ prob }}</v-card-text>
      <!-- <SVGElement name='/assets/temp.svg' /> -->
      <img
        :src="svg_path"
        class="justify-center"
      >
    </v-card>
    </v-col>
    </v-row>
    </v-container>
  </swiper-slide>
</template>

<script>
import SVGElement from "@/components/SVGElement.vue";
export default {
  name: "ImageCard",
  props: ["rank","src","prob",'id'],
  components: { SVGElement },
  data() {
    return {
      default_src: require("~/assets/temp.svg"), //imgタグで読み込む
      svg_path: ""
    };
  },
  created:function(){
    // 画像のpathが同じ名前になるのでクエリパラメータでタイムスタンプつける必要あり
    this.svg_path="file://" + this.src + "?" + new Date().getTime();
    // console.log(this.svg_path);
  },
};
</script>

<style>
</style>