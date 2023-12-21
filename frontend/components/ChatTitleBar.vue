<template>
  <div
    class="flex justify-between items-center bg-white dark:bg-gray-700 dark:text-slate-300 h-14 sm:h-16 pl-2 sm:px-4 border-b"
  >
    <div class="grow inline-flex items-center space-x-2">
      <div
        class="icon-btn flex-none block sm:hidden dark:hover:text-gray-600"
        @click="toggleSideBar()"
      >
        <HamburgerButton size="22" />
      </div>
      <div class="flex-none hidden sm:block">
        <Message size="24" />
      </div>
      <input
        ref="titleInputDom"
        class="border px-2 py-1 rounded-md"
        v-if="editTitle"
        v-model.trim="editTitle"
        type="text"
        name="title"
        @focusout="exitEditing"
        @keydown.enter="exitEditing"
      />
      <div v-else class="grow flex inline-flex w-1">
        <div
          class="overflow-hidden whitespace-nowrap text-lg text-ellipsis"
          @dblclick="enterEditing"
        >
          {{ title }}
        </div>
      </div>
    </div>
    <div class="flex-none inline-flex items-center">
      <div
        class="icon-btn hidden sm:block dark:hover:text-gray-600"
        @click="store.showHelp = true"
      >
        <Help size="22" />
      </div>
      <div class="icon-btn dark:hover:text-gray-600" @click="clearMessages">
        <Clear size="22" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  HamburgerButton,
  Message,
  Clear,
  Help,
} from "@icon-park/vue-next";
import { useChatStore } from "@/stores/chat";
import type { ConversationItem } from "@/types";

const store = useChatStore();
const i18n = useI18n();

const titleInputDom = ref<HTMLInputElement>();
const editTitle = ref("");
const clearConfirmMessage = i18n.t("ChatTitleBar.clearMessages.confirm");

const title = computed(
  () => store.conversation?.title ?? i18n.t("ChatTitleBar.initialTitle")
);


function enterEditing() {
  if (!store.conversation?.id) return;
  editTitle.value = store.conversation?.title ?? title.value;
  nextTick(() => titleInputDom.value?.focus());
}

async function exitEditing() {
  const chatId = store.conversation?.id;
  if (!editTitle.value) return;
  if (!chatId) return;
  await store.reConversationTitle(chatId, editTitle.value);
  editTitle.value = "";
}

function clearMessages() {
  if (confirm(clearConfirmMessage)) {
    store.clearMessages((store.conversation as ConversationItem).id);
  }
}
</script>

<style scoped>
.icon-btn {
  @apply p-2.5 rounded-md sm:hover:bg-slate-200 active:bg-slate-200 cursor-pointer;
}
</style>
