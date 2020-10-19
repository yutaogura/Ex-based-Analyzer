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
      console.log(this.name)
      return () => import(`~/assets/temp.svg`)
    }
  }
}
</script>