import { defineStore } from "pinia";
import type {
   ChatMessage, ConversationItem, CreateConversationRequest, ConversationHistory, ChatMessageItem, ChatCompletionRequest, ErrorResponse, ConversationUpdate
} from "@/types";

export const useChatStore = defineStore("chat", () => {
  const decoder = new TextDecoder("utf-8");

  const i18n = useI18n();

  let controller: AbortController;

  const showSetting = ref(false);
  const showHelp = ref(false);
  const runtimeConfig = useRuntimeConfig();
  const conversations = ref<ConversationItem[]>([]);
  const conversation = ref<ConversationItem>();
  const messages = ref<ChatMessageItem[]>([])
  const messageContent = ref("");
  const talkingChats = ref(new Set<string>([]));

  // talking

  const talking = computed(
    () => talkingChats.value.has(conversation.value?.id ?? "") ?? false
  );

  function startTalking(conversation_id: string) {
    talkingChats.value.add(conversation_id);
  }

  function endTalking(conversation_id: string) {
    talkingChats.value.delete(conversation_id);
  }

  // chat

  async function getAllConversation() {
    try {
      const res = (await $fetch(
        '/api/conv/conversation',
        {
          method: "GET",
        }
      )) as ConversationItem[]
      conversations.value = res;
    } catch {
      conversations.value = []
    }
    conversation.value = undefined
  }

  async function createConversation() {
    conversation.value = undefined;
    const convItem = (await $fetch(
      '/api/conv/new',
      {
        method: 'POST',
        body: JSON.stringify({
          title: "new chat"
        } as CreateConversationRequest)
      }
    )) as ConversationItem
    let len = conversations.value.push(convItem)
    conversation.value = conversations.value[len-1]
    return convItem.id
  }


  async function openConversation(item: ConversationItem) {
    // console.log(item);
    conversation.value = item;
    await getConversationMessages(item.id);
  }

  async function removeConversation(conversationId: string) {
    if (!confirm(i18n.t("removeChatConfirm"))) return;
    await $fetch(
      `/api/conv/delete/${conversationId}`,
      {
        method: "post",
      }
    )
    messages.value = []
    await getAllConversation();
  }

  async function reConversationTitle(conversationId: string, title: string) {
    await $fetch(
      '/api/conv/upgrade',
      {
        method: 'post',
        body: JSON.stringify({
          title: title
        } as CreateConversationRequest)
      }
    )
    await getAllConversation();
    const conv = conversations.value.find((item) => item.id === conversationId);
    if (conv) openConversation(conv);
  }
    

  async function getConversationMessages(conversation_id: string) {
    const mapping = (await $fetch(
      `/api/conv/messages/${conversation_id}`,
      {
        method: "get"
      }
    )) as ConversationHistory
    const res = []
    let node = mapping.curr_node
    while(node) {
      res.unshift(mapping.messages[node])
      node = mapping.messages[node].parent
    }
    messages.value = res
  }

  async function clearMessages(conversation_id: string) {
    await $fetch(
      `/api/conv/clear/${conversation_id}`,
      {
        method: "post"
      }
    )
    messages.value = []
    await getConversationMessages(conversation_id);
  }

  function stop() {
    controller?.abort();
  }

  function clearSendMessageContent() {
    messageContent.value = "";
  }

  async function gen_title(conversationId: string) {
    const msg = messages.value.map(({ role, content }) => { return { role: role, content: content } as ChatMessage })
    console.log(msg)
    await fetch(
      `/api/conv/gen-title/${conversationId}`,
      {
        method: "post",
        body: JSON.stringify(msg)
      }
    ).then(response => {
      if (response.ok) {
        response.json().then((data: ConversationUpdate) => {
          const conv = conversations.value.find((item) => item.id === conversationId);
          if (conv) {
            conv.title = data.title
            conversation.value = conv
          }
        })
      } else {
        response.json().then((data: ErrorResponse) => {
          console.log(data.detail)
        });
      }
    }).catch((e) => {
      console.log(e)

    });

  }


  async function createMessage(conversaionId: string, message: ChatMessage) {
    const res = (await $fetch(
      `/api/conv/message/${conversaionId}`,
      {
        method: 'post',
        body: message
      }
    )) as ChatMessageItem
    return res
  }

  async function sendMessage(message: ChatMessage) {
    if (talking.value) return;
    if (!message?.content.trim()) return;

    let conversationId = conversation.value?.id;
  
    if (!conversationId) {
      conversationId = await createConversation()
    }

    const setting = loadSetting();
    if (!setting) {
      showSetting.value = true;
      return;
    }
    const history_length = setting.history_length
    // 开始对话 (start a conversation)
    clearSendMessageContent();

    // 追加到消息队列 (append to message queue)
    messages.value.push(await createMessage(conversationId, message as ChatMessage) as ChatMessageItem)

    const len = messages.value.push({
      role: "assistant",
      content: "",
    } as ChatMessageItem)

    console.log(messages.value)

    // 用于主动中断请求 (for unsolicited interrupt requests)
    controller = new AbortController();
    let content = "";
    try {
      startTalking(conversationId);
      // 发送请求 (send request)
      const { status, statusText, body } = await fetch(
        `/api/chat/${conversationId}`,
        {
          method: "post",
          body: JSON.stringify({
            model: "",
            messages: messages.value.slice(Math.max(0, (len-history_length)*2), len - 1),
            temperature: setting.temperature || Number(runtimeConfig.public.defaultTemperature),
            stream: true,
            top_p: setting.top_p || Number(runtimeConfig.public.defaultTop_p),
            top_k: setting.top_k || Number(runtimeConfig.public.defaultMax_length),
            max_length: setting.max_length || Number(runtimeConfig.public.defaultMax_length),
          } as ChatCompletionRequest),
          signal: controller.signal,
        }
      );

      // 读取 Stream
      
      const reader = body?.getReader();

      let parsedCount = 0;
      let concatenatedValue = new Uint8Array();

      while (reader) {
        const { value } = await reader.read();

        // concatenate with the previous value
        concatenatedValue = new Uint8Array([...concatenatedValue, ...value!]);

        const text = decoder.decode(concatenatedValue);

        // 处理服务端返回的异常消息并终止读取 (Handle the exception message returned by the server and terminate the read)
        if (status !== 200) {
          content += `${status}: ${statusText}\n`;
          content += text;
          console.log(content)
          messages.value[len - 1].content = content
          return;
        }

        // 读取正文 (read text)
        const line = text
          .split(/\r?\n/)
          .map((line) => line.replace(/(\n)?^data:\s*/, "").trim()) // remove prefix
          .filter((line) => line !== ""); // remove empty lines
        for (let i = parsedCount; i < line.length; i++) {
          if (line[i] === "[DONE]") return;

          try {
            const data = JSON.parse(line[i]);
            content += data.choices[0].delta.content ?? "";
            ;
            parsedCount++;
            messages.value[len-1].content = content
          } catch (e) {
            console.warn("Could not JSON parse stream message", e);
            continue;
          }
        }
      }
    } catch (e: any) {
      // 主动终止时触发 (Triggered on active termination)
      console.log(e)
        messages.value[len-1].content += (`\n\n**${
          e.name === "AbortError" ? i18n.t("ChatStop.message") : e.message}`)
    } finally {
      endTalking(conversationId);
      const msg = await createMessage(conversationId, {content: content, role: 'assistant'} as ChatMessage)
      console.log(msg)
      messages.value[len - 1] = msg
      console.log(messages.value.length)
      if (messages.value.length == 2 || messages.value.length%10 == 0) {
        gen_title(conversationId)
      }
    }
  }

  // locale

  function getLocale() {
    const setting = loadSetting();
    return (setting && setting.locale) ?? i18n.getBrowserLocale() ?? "en";
  }

  // color mode

  function getColorMode() {
    const setting = loadSetting();
    return (setting && setting.colorMode) ?? "system";
  }


  return {
    showSetting,
    showHelp,
    conversations,
    conversation,
    messages,
    messageContent,
    talking,
    gen_title,
    stop,
    openConversation,
    reConversationTitle,
    getConversationMessages,
    getAllConversation,
    createConversation,
    clearMessages,
    removeConversation,
    sendMessage,
    getLocale,
    getColorMode,
  };
});