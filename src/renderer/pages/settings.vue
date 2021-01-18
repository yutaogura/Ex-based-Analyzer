<template>
  <div class="main_content">
    <h1>Settings</h1>
    <p>各種設定をするよ</p>
    <v-divider></v-divider>
    <br>
    <v-text-field value="py/svg/" label="svg dir path" ></v-text-field>
    <v-text-field value="py/temp/" label="pkl dir path" ></v-text-field>
    <v-text-field value="py/incremental_chart.py" label="parser path" ></v-text-field>
    <v-text-field value="py/pcfg.txt" label="pcfg path" ></v-text-field>
    <v-text-field value="py/tonic.txt" label="tonic path" ></v-text-field>
     <v-text-field value=30 label="Drawing num" ></v-text-field>        
  </div>
</template>