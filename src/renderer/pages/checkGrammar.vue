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
      :items-per-page="10"
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

const fs = require("fs");
const PCFG_FILE = "py/pcfg.txt"

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
      prolong_data: []
      // [
      //   {
      //     name: "A7 -> A7 A7",
      //     probability: 0.5,
      //     isProlong: true,
      //   },
      //   {
      //     name: "C7 -> C7 C7",
      //     probability: 0.2,
      //     isProlong: true,
      //   },
      //   {
      //     name: "F7 -> F7 F7",
      //     probability: 0.1,
      //     isProlong: true,
      //   },
      //   {
      //     name: "B7 -> B7 B7",
      //     probability: 0.7,
      //     isProlong: true,

      //   },
      // ],
    };
  },
  created() {
    console.log('----- created -----')
    try {
        let target = fs.readFileSync(PCFG_FILE,'utf-8');
        const line = target.split('\n'); //１行ずつ分割
        for(var i in line){
          if(line[i]){
            var lh = line[i].split("-> ")[0];
            var rh = line[i].split("-> ")[1];
            var rhl = rh.split(" ")[0];
            var rhr = rh.split(" ")[1];
            var prob = rh.split(" ")[2];
            prob = prob.replace(/\[|\]/g,"");

            var rule = lh + " -> " + rhl +" "+ rhr;
            var data = {"name": rule,
                        "probability":prob,
                        "isProlong": true};
            this.prolong_data.push(data);
          }
        }
        
      } catch (e) {
        console.log(e);
      }
  },
};
</script>
<style>
</style>