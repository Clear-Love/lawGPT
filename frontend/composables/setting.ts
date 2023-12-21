import type { ConversationSettingItem, ConversationSettingOption } from "../types/chat/setting";

const key = "chatSetting";

export async function saveSetting(setting: ConversationSettingOption) {
  localStorage.setItem(key, JSON.stringify({ ...setting }));
}

export function loadSetting(): ConversationSettingItem | undefined {
  const settingString = localStorage.getItem(key);
  if (settingString) {
    return JSON.parse(settingString);
  }
}
