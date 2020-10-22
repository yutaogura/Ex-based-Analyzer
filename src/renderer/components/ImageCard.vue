<template>
  <swiper-slide>
    <v-container >
    <v-row>
    <v-col>   
    <v-card>
      <!-- <v-card-text>tree {{ num }} {{src}} prob:NaN </v-card-text> -->
      <v-card-text>{{ return_file_name(src) }} </v-card-text>
      <!-- <SVGElement name='/assets/temp.svg' /> -->
      <img
        :src="imageSrc(src)"
        class="justify-center"
      >
    </v-card>
    </v-col>
    </v-row>
    </v-container>
  </swiper-slide>
</template>

<script>
import SVGElement from "@/components/SVGElement.vue"
export default {
  name: "ImageCard",
  props: ["num","src"],
  components: { SVGElement },
  data() {
    return {
      default_src: require("~/assets/temp.svg"), //imgタグで読み込む
    };
  },
  methods:{
    return_file_name: function(src){
      return src.replace(/^.*[\\\/]/, '')
    },
    imageSrc: function(src){
      if(src){
        src = "file://" + src;
        console.log(src);
        return src;
      }else{
        console.log("hogehoge" + this.default_src);
        return this.default_src;
      }
    }
  }
};
</script>

<style>
</style>