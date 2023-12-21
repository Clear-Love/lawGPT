export type ChatSettingType = "default" | "global" | "chat";

export type ColorMode = "system" | "light" | "dark";

export interface ConversationSettingItem extends ConversationSettingOption {
  id: number;
}

export interface ConversationSettingOption extends ConversationSetting {
  type: ChatSettingType;
}

export interface ConversationSetting {
  top_k?: number;
  top_p?: number;
  max_length?: number;
  history_length: number;
  temperature: number;
  locale: string;
  colorMode: ColorMode;
}
