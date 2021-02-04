<template>
  <swiper-slide>
    <v-container >
    <v-row>
    <v-col>   
    <v-card>
      <!-- <v-card-text>tree {{ num }} {{src}} prob:NaN </v-card-text> -->
      <v-card-text>{{ rank }} : {{ prob }} : {{id}}</v-card-text>
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
    this.svg_path="file://" + this.src + "?" + new Date().getTime();
    console.log(this.svg_path);
  },
  // methods:{
  //   getSrc: function(){
  //     console.log("I was called!")
  //     if(src){
  //       src = "file://" + src;
  //       return this.svg_path;
  //     }else{
  //       return this.default_src;
  //     }
  //   }
  // }
};
</script>

<style>
</style>