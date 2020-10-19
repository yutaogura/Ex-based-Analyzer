<template>
  <swiper-slide>
    <v-container >
    <v-row>
    <v-col>   
    <v-card>
      <v-card-text>tree {{ num }} {{src}} prob:NaN </v-card-text>
      <SVGElement :name="src" />
      <!-- <v-img
        v-bind:src="image_src"
        max-width="100"
        class="justify-center"
      /> -->
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
      image_src: require("@/assets/t.svg"), //imgタグで読み込む
    };
  },
};
</script>

<style>
</style>