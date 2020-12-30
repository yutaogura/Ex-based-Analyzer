<template>
  <v-app>
    <!-- <app-header /> -->
    <client-only>
    <div id="demo" :class="[{ collapsed: collapsed }]">
    <nuxt />
    </div>

    <sidebar-menu
      class="sidebar"
      :menu="menu"
      :collapsed="collapsed"
      @item-click="onItemClick"
      @toggle-collapse="onCollapse"
    >
      <span slot="toggle-icon"><font-awesome-icon icon="arrows-alt-h" /></span>
      <span slot="dropdown-icon">dropdown-icon</span>
    </sidebar-menu>
    <div v-if="!collapsed" class="sidebar-overlay" @click="collapsed = true" />
    </client-only>
  </v-app>
</template>

<script>
import appHeader from "@/components/header";
import { mdiMidiPort } from "@mdi/js";
export default {
  // components: { appHeader }
  data() {
    return {
      menu: [
        {
          header: true,
          title: "Ex-based Chord Sequence Analyzer",
          hiddenOnCollapse: true,
        },
        {
          href: "/",
          title: "Tree analysis",
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "tree",
            },
          },
        },
        {
          href: "/installation",
          title: "Change Probability",
          disabled: false,
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "sliders-h",
            },
          },
        },
        {
          //href: "/installtion",
          title: "Check Grammar",
          disabled: true,
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "spell-check",
            },
          },
        },
        {
          //href: "/",
          title: "Settings",
          disabled: true,
          icon: {
            element: "font-awesome-icon",
            attributes: {
              // icon props:
              icon: "cogs",
            },
          },
        },
        {
          header: true,
          title: "Others",
          hiddenOnCollapse: true,
        },
        {
          href: "/connectMidi",
          title: "Connect MIDI Keyboard",
          disabled: false,
          icon: {
            element: "v-icon",
            class: ["white--text"], 
            text: mdiMidiPort,
          },
        },
        // {
        //   href: "/",
        //   title: "Dropdown Page",
        //   icon: "list-ul",
        //   child: [
        //     {
        //       href: "/",
        //       title: "Sub Page 01",
        //       //icon: "fa fa-file-alt"
        //     },
        //     {
        //       href: "/",
        //       title: "Sub Page 02",
        //       //icon: "fa fa-file-alt"
        //     },
        //   ],
        // },
      ],
      collapsed: true,
      show: false,
      externalContent: "",
      sequence: [],
      sequence_data: "",
      loading: false,
    };
  },
  methods: {
    onItemClick(e, i) {
      console.log("onItemClick");
    },
    onCollapse(c) {
      console.log("onCollapse");
      this.collapsed = c;
    },
  }
};
</script>

<style>
* {
  margin: 0px;
  padding: 0px;
}

.sidebar-overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background-color: #000;
  opacity: 0.5;
  z-index: 900;
}

.v-icon__svg{ 
  width: 30px;
  height:30px;
  }

#demo {
  padding-left: 350px;
  transition: 0.3s ease;
}
#demo.collapsed {
  padding-left: 50px;
}


.v-sidebar-menu .vsm--mobile-bg{
    background-color: #4285f4CC;
}

h1{
  text-align: center;
}
</style>
