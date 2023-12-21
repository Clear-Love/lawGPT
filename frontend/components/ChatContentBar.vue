<template>
  <div class="flex flex-col p-3 pb-0 max-w-full relative">
    <ChatTitleBar />
    <ChatMessageList class="flex-1" v-if="store.messages.length" />
    <template v-else>
        <ChatWelcome class="flex-1" />
    </template>
    <div class="absolute sm:pb-2 bottom-0 left-0 right-0 bg-gradient-to-t from-white dark:from-gray-700 flex-2">
      <ChatStop v-show="store.talking" />
      <ChatSendBar />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useChatStore } from "@/stores/chat";

const store = useChatStore();

</script>
