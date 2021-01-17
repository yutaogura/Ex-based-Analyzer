<template>
  <div class="main_content">
    <h1>Check Grammar</h1>
    <p>和声文法の適用確率を確認</p>
    <v-divider></v-divider>
    <p></p>
    <h2>Prolongation rule</h2>
    <v-data-table
      :headers="headers"
      :items="prolong_data"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>
    <v-divider></v-divider>
    <p></p>
    <h2>Preparation rule</h2>
    <v-data-table
      :headers="headers"
      :items="prolong_data"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>
  </div>
</template>
<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "rule",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "prob.", value: "probability" },
      ],
      prolong_data: [
        {
          name: "A7 -> A7 A7",
          probability: 0.5,
          isProlong: true,
        },
        {
          name: "C7 -> C7 C7",
          probability: 0.2,
          isProlong: true,
        },
        {
          name: "F7 -> F7 F7",
          probability: 0.1,
          isProlong: true,
        },
        {
          name: "B7 -> B7 B7",
          probability: 0.7,
          isProlong: true,

        },
      ],
    };
  },
};
</script>
<style>
</style>