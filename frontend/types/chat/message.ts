import type { ConversationItem } from "@/types";

export type ChatRole = "user" | "assistant" | "system";

export interface ChatMessage {
  role: ChatRole;
  content: string;
}

export interface ChatMessageItem extends ChatMessage {
  id?: string
}

export interface ChatMessageResponse extends ChatMessage {
  id: string
  conversation_id?: ConversationItem["id"];
  parent: string;
  create_time?: number;
}

export interface SearchResponse {
  docs: string[]
}