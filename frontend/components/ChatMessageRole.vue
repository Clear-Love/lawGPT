<template>
  <div class="flex" :class="{ 'flex-row-reverse': item.role === 'user' }">
    <ChatAvatar class="item-gap" :role="item.role" />
    <div class="group item-gap overflow-x-hidden" v-if="item.content">
      <div
        class="prose break-words px-3 py-2 rounded-lg text-sm sm:text-base overflow-x-auto"
        :class="
          item.role === 'user'
            ? 'ml-auto bg-blue-500 dark:bg-blue-700 text-white dark:text-slate-200 prose-invert'
            : 'mr-auto bg-slate-100 dark:bg-slate-500 text-slate-700 dark:text-slate-200'
        "
        v-html="md.render(item.content)"
      />
      <div class="flex items-center space-x-2">
        <CopyText
          class="mt-1.5 visible sm:invisible group-hover:visible"
          :content="item.content"
        />
      </div>
    </div>
    <ChatMessageLoding class="item-gap" v-else />
  </div>
</template>

<script setup lang="ts">
import type { ChatMessageItem } from "@/types";

defineProps<{
  item: ChatMessageItem;
}>();

</script>

<style>
.item-gap {
  @apply m-1.5;
}
</style>
