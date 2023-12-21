<template>
  <div class="flex justify-center mb-6">
    <div
      class="w-11/12 sm:w-4/5 p-2 bg-slate-100 text-xs text-slate-500 border rounded-lg"
    >
      {{ item.content }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessageItem } from "@/types";

defineProps<{
  item: ChatMessageItem;
}>();
</script>

<style scoped></style>
