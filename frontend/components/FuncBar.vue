<template>
  <div class="pt-2 border-t">
    <div
      class="bar-btn dark:hover:text-gray-600"
      v-for="item in funcs"
      :key="item.type"
      @click="clickBtn(item.type)"
    >
      <component :is="item.icon" />
      <div>{{ $t(`FuncBar.${item.type}`) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Plus, Setting, Github, Logout} from "@icon-park/vue-next";
import { useChatStore } from "@/stores/chat";
import useUserStore from "~/stores/auth";

const store = useChatStore();
const auth = useUserStore()

const funcs = [
  { type: "chat", icon: Plus },
  { type: 'search', icon: Plus},
  { type: "setting", icon: Setting },
  { type: "github", icon: Github },
  { type: "logout", icon: Logout}
];

async function clickBtn(type: string) {
  if (type === "chat") {
    store.createConversation('chat');
    toggleSideBar();
  }else if (type == 'search') {
    store.createConversation('search')
    toggleSideBar();
  } else if (type === "setting") {
    store.showSetting = true;
    toggleSideBar();
  } else if (type === "github") {
    open("https://github.com/Clear-Love/lawGPT", "_blank");
  } else if (type === 'logout') {
    auth.logout()
  }
}
</script>

<style scoped></style>
