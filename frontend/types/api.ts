import type { ChatMessage } from "./chat";

export type ApiRequestModel = "models" | "chat" | "text";

export interface ErrorResponse {
  detail: string
}

export interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  temperature: number;
  top_p: number;
  top_k: number;
  max_length: number;
  stream: boolean;
}
