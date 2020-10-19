<template>
  <v-app>
    <no-ssr>
      <div class="e-nuxt-container">
        <v-text-field label="chord sequence" outlined clearable>
          <template v-slot:append-outer>
            <v-btn color="primary" @click="showDialog">Analyse</v-btn>
          </template>
        </v-text-field>
        <div v-for="(value, index) in sequence" :key="index">
          <each-step :sequence="sequence.slice(0, index + 1)" />
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
      sequence: ["Cmaj7", "D7", "Dmin7", "G7", "Cmaj7"],
    };
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.$swiper;
    },
  },
  methods: {
    showDialog: function (event) {
      const { dialog } = require("electron").remote;
      console.log(dialog);
      dialog.showErrorBox("Error", "まだ作っていません!");
    },
  },
};
</script>




<style>
.e-nuxt-container {
  padding: 10px;
  min-height: calc(100vh);
  background: linear-gradient(to right, #ece9e6, #ffffff);
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
