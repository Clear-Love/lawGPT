<template>
  <div
    class="sm:flex px-1.5 sm:px-6 pt-6 sm:space-x-4 space-y-6 sm:space-y-0 overflow-y-hidden"
  >
    <div class="sm:flex-1 space-y-4" v-for="item of examples">
      <div class="flex flex-col items-center space-y-2">
        <component class="text-slate-400" :is="item.icon" size="20" />
        <div class="font-bold text-base dark:text-slate-300">
          {{ $t(`ChatWelcome.${item.id}.title`) }}
        </div>
      </div>
      <div
        class="flex justify-center items-center p-2 h-20 rounded bg-slate-100 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600 text-center cursor-pointer"
        v-for="exa of ($tm(`ChatWelcome.${item.id}.examples`) as ChatMessageTemplate[])"
        @click="sendMessage(exa.message, exa.type)"
      >
        {{ $rt(exa.title) }}
      </div>
    </div>
    <div class="h-32" />
  </div>
</template>

<script setup lang="ts">
import { Tool, Chip, Search } from "@icon-park/vue-next";
import type { Icon } from "@icon-park/vue-next/lib/runtime";
import { useChatStore } from "@/stores/chat";
import type { ChatMessage, ChatRole } from "@/types";

interface ChatMessageTemplate {
  title: string;
  type: 'chat' | 'search';
  message: ChatMessage;
}

interface ChatMessageTemplateGroup {
  id: string;
  icon?: Icon;
}

const store = useChatStore();
const i18n = useI18n();

const examples: ChatMessageTemplateGroup[] = [
  {
    id: "tool",
    icon: Tool,
  },
  {
    id: "rolePlaying",
    icon: Chip,
  },
  {
    id: "casualChat",
    icon: Search,
  },
];

async function sendMessage(message: ChatMessage, type: 'chat' | 'search') {
  if (!store.conversation) {
    await store.createConversation(i18n.rt(type) as 'chat' | 'search')
  }
  store.sendMessage({
    role: i18n.rt(message.role) as ChatRole,
    content: i18n.rt(message.content),
  });
}

defineEmits(["clickExamples"]);
</script>
