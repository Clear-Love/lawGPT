<template>
  <div class="h-3/4 overflow-y-auto">
    <div class="m-6 mb-2 text-sm text-slate-500">
      {{ $t("ChatList.conversations") }}
    </div>
    <div
      :class="[
        'group bar-btn flex justify-between dark:hover:text-gray-600',
        { 'bg-slate-200 dark:bg-gray-700': store.conversation === item },
      ]"
      v-for="item in convs"
      :key="item.id"
      @click="openChat(item)"
    >
      <div class="max-w-[85%] flex items-center space-x-1">
        <IconMessage />
        <span class="overflow-hidden whitespace-nowrap text-ellipsis">
          {{ item.title }}
        </span>
      </div>
      <CloseOne
        class="invisible group-hover:visible text-rose-400"
        @click.stop.left="closeChat(item)"
      />
    </div>
    <div class="m-6 mb-2 text-sm text-slate-500">
        {{ $t("ChatList.searchs") }}
      </div>
      <div
        :class="[
          'group bar-btn flex justify-between dark:hover:text-gray-600',
          { 'bg-slate-200 dark:bg-gray-700': store.conversation === item },
        ]"
        v-for="item in searchs"
        :key="item.id"
        @click="openChat(item)"
      >
        <div class="max-w-[85%] flex items-center space-x-1">
          <IconMessage />
          <span class="overflow-hidden whitespace-nowrap text-ellipsis">
            {{ item.title }}
          </span>
        </div>
        <CloseOne
          class="invisible group-hover:visible text-rose-400"
          @click.stop.left="closeChat(item)"
        />
      </div>
  </div>
</template>

<script setup lang="ts">
import {
  Message as IconMessage,
  CloseOne,
} from "@icon-park/vue-next";
import { useChatStore } from "@/stores/chat";
import type { ConversationItem } from "@/types";

const store = useChatStore();

const convs = computed(() => store.conversations.filter(item => item.type === 'chat'))
const searchs = computed(() => store.conversations.filter(item => item.type === "search"))

async function openChat(item: ConversationItem) {
  store.$patch({ showSetting: false, conversation: item });
  await store.getConversationMessages(item.id);
  toggleSideBar();
}

async function closeChat(item: ConversationItem) {
  await store.removeConversation(item.id);
  if (store.conversations.length > 0) {
    await openChat(store.conversations[0]);
  }
}
</script>

<style scoped></style>
