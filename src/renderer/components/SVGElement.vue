<template>
  <component :is="svg"/>
</template>

<script>
export default {
  name: "SVGElement",
  props: {
    name: {
      type: String,
    },
  },
  computed: {
    svg() {
      //console.log(this.name)
      //console.log(import(this.name))
      //let a = this.name;
      //console.log(`~/${a}`);
      //import("~"+a).then((module) =>{console.log(module)});
      return () => import('~/assets/temp.svg');
    }
  }
}
</script>