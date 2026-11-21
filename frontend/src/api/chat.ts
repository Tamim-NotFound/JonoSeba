import { apiPost } from "./client";

export interface ChatHistoryMessage {
  role: "user" | "model";
  content: string;
}

export interface ChatResponse {
  reply: string;
  model: string;
}

export function askJonoSeba(
  message: string,
  history: ChatHistoryMessage[],
): Promise<ChatResponse> {
  return apiPost<ChatResponse>("/chat", {
    message: message.trim(),
    history: history.slice(-20),
  });
}
