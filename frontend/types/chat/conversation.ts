import type { ChatMessageResponse } from "@/types";

export interface ConversationItem extends ConversationOption {
  id: string;
}

export interface ConversationUpdate {
  title: string;
}

export interface ConversationOption {
  title?: string;
  create_time?: Date;
  update_time?: Date;
  type: 'chat' | 'search';
}

export interface CreateConversationRequest {
  title: string;
  type: 'chat' | 'search';
}

export interface ConversationHistory {
  conversation_id: string
  messages: Record<string, ChatMessageResponse> // 消息链表
  curr_node: string //消息尾部数据
}