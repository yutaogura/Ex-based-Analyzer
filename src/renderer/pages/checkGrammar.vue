<template>
  <div class="main_content">
    <h1>Check Grammar</h1>
    <p>display all Harmonic Grammar</p>
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
      :items="preparation_data"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>
  </div>
</template>
<script>

const fs = require("fs");
const PCFGprl_FILE = "py/pcfg_prl.txt"
const PCFGprep_FILE = "py/pcfg_prep.txt"

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
      prolong_data: [],
      preparation_data: [],
    };
  },
  created() {
    console.log('----- created -----')
    try {
        var target = fs.readFileSync(PCFGprl_FILE,'utf-8');
        var line = target.split('\n'); //１行ずつ分割
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

        var target = fs.readFileSync(PCFGprep_FILE,'utf-8');
        var line = target.split('\n'); //１行ずつ分割
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
                        "isProlong": false};
            this.preparation_data.push(data);
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