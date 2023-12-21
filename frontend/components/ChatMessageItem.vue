<template>
  <div>
    <ChatMessageSystem
      v-if="item.role === 'system'"
      :item="item"
    />
    <ChatMessageRole v-else :item="item" />
  </div>
</template>

<script setup lang="ts">
import type { ChatMessageItem } from "@/types";

defineProps<{
  item: ChatMessageItem;
}>();
</script>

<style scoped></style>
