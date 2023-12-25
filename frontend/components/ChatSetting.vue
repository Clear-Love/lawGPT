<template>
  <div class="flex flex-col p-6 space-y-6 overflow-y-scroll">
    <div class="m-6 mb-2 text-sm text-slate-500">
      {{ $t("ChatSetting.conversations") }}
    </div>
    <!-- temperature -->
    <div>
      <label class="space-x-3">
        <span>{{ $t("ChatSetting.temperature") }}</span>
        <span>{{ setting.temperature }}</span>
      </label>
      <input
        type="range"
        v-model.number="setting.temperature"
        min="0"
        max="1"
        step="0.1"
      />
    </div>
    <!-- top_k -->
    <div>
      <label class="space-x-3">
        <span>{{ $t("ChatSetting.top_k") }}</span>
        <span>{{ setting.top_k }}</span>
      </label>
      <input
        type="range"
        v-model.number="setting.top_k"
        min="4"
        max="10"
        step="1"
      />
    </div>
    <div>
      <label class="space-x-3">
        <span>{{ $t("ChatSetting.history_length") }}</span>
        <span>{{ setting.history_length }}</span>
      </label>
      <input
        type="range"
        v-model.number="setting.history_length"
        min="4"
        max="64"
        step="1"
      />
    </div>
    <!-- top_p -->
    <div>
      <label class="space-x-3">
        <span>{{ $t("ChatSetting.top_p") }}</span>
        <span>{{ setting.top_p }}</span>
      </label>
      <input
        type="range"
        v-model.number="setting.top_p"
        min="0"
        max="1"
        step="0.1"
      />
    </div>
    <div class="m-6 mb-2 text-sm text-slate-500">
      {{ $t("ChatSetting.searchs") }}
    </div>
    <!-- top_k -->
      <div>
        <label class="space-x-3">
          <span>{{ $t("ChatSetting.search_top_k") }}</span>
          <span>{{ setting.search_top_k }}</span>
        </label>
        <input
          type="range"
          v-model.number="setting.search_top_k"
          min="4"
          max="10"
          step="1"
        />
      </div>
    <!-- language -->
    <div>
      <label class="space-x-3">
        <span>{{ $t("ChatSetting.language") }}</span>
      </label>
      <select v-model="setting.locale">
        <option v-for="locale in availableLocales" :value="locale.code">
          {{ locale.name }}
        </option>
      </select>
    </div>

    <!-- action buttons -->
    <div>
      <label class="space-x-3">
        <span>{{ $t("ChatSetting.colorMode.label") }}</span>
      </label>
      <select v-model="setting.colorMode">
        <option value="system">{{ $t("ChatSetting.colorMode.system") }}</option>
        <option value="light">{{ $t("ChatSetting.colorMode.light") }}</option>
        <option value="dark">{{ $t("ChatSetting.colorMode.dark") }}</option>
      </select>
    </div>
    <div class="space-x-3">
      <button class="main-button" @click="save">
        {{ $t("ChatSetting.save") }}
      </button>
      <button class="second-button" @click="store.showSetting = false">
        {{ $t("ChatSetting.back") }}
      </button>
    </div>
</div>
</template>

<script setup lang="ts">
import type { ConversationSettingOption } from "@/types";
import type { LocaleObject } from "@nuxtjs/i18n/dist/runtime/composables";
import { useChatStore } from "~/stores/chat";

const runtimeConfig = useRuntimeConfig();
const store = useChatStore();
const i18n = useI18n();
const availableLocales = i18n.locales.value as LocaleObject[];

const setting = ref<ConversationSettingOption>({
  top_k: Number(runtimeConfig.public.defaultTop_k),
  top_p: Number(runtimeConfig.public.defaultTop_p),
  max_length : Number(runtimeConfig.public.defaultMax_length),
  temperature: Number(runtimeConfig.public.defaultTemperature),
  history_length: Number(runtimeConfig.public.defaultHistory_length),
  search_top_k: Number(runtimeConfig.public.defaultSearchTop_k),
  locale: i18n.getBrowserLocale()!,
  colorMode: "system",
  type: "global",
});

const colorMode = useColorMode();

onMounted(() => {
  setting.value = loadSetting() ?? setting.value;
});

async function save() {
  await saveSetting(setting.value);
  i18n.setLocale(store.getLocale());
  colorMode.preference = store.getColorMode();
  store.showSetting = false;
}
</script>

<style scoped>
label:not(.radio-switch) {
  @apply block mb-2 text-sm font-medium text-gray-900 dark:text-slate-300;
}

input[type="password"],
input[type="text"],
select {
  @apply bg-gray-50 border border-gray-300 dark:border-gray-500 text-gray-900 dark:text-slate-300 dark:bg-gray-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5;
}

input[type="range"] {
  @apply w-full h-2 bg-gray-200 dark:bg-gray-500 rounded-lg appearance-none cursor-pointer;
}

button {
  @apply font-medium rounded-lg text-sm px-5 py-2.5 text-center;
}

.main-button {
  @apply text-white dark:text-slate-300 bg-blue-700 hover:bg-blue-800;
}

.second-button {
  @apply bg-white dark:bg-slate-400 text-gray-900 hover:bg-gray-50 dark:hover:bg-slate-300 border shadow-sm;
}
</style>
