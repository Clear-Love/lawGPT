import asyncio
import sys
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from lawgpt.log import get_logger
from lawgpt.models.dbModels import User
from lawgpt.models.reqModels import ChatCompletionRequest, ChatMessage, CreateContentSchema, DeltaMessage
from lawgpt.models.respModels import ChatCompletionResponse, ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice
from sse_starlette.sse import EventSourceResponse
from transformers import AutoTokenizer, AutoModel
from lawgpt.services.chatService import ChatService
from lawgpt.services.vecDBService import vecDBService
from lawgpt.utils.chatglm import ChatGLM
from lawgpt.utils.user_manager import current_active_user
from langchain.prompts import PromptTemplate
from lawgpt.config import settings

router = APIRouter()
logger = get_logger(__name__)
_service = ChatService()
vecDB = vecDBService()
model_dir = settings.LLM_MODEL
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).cuda()
model.eval()
chatglm = ChatGLM()
chatglm.tokenizer = tokenizer
chatglm.model = model


TEMPLATE = """
            {docs}
            以上是你自己掌握的法律知识，你现在将扮演一名专业的法律助手，如果法律知识未与问题内容相关则无视该法律知识，请用你掌握的法律知识作为参考回答以下问题，问题是：
            “{query}”
        """
resp_prompt = PromptTemplate(
    input_variables=["query", "docs"],
    template=TEMPLATE
)


@router.post("/chat/{conversation_id}", response_model=ChatCompletionResponse)
async def create_chat_completion(conversation_id: str,
                                 request: ChatCompletionRequest,
                                 current_user: User = Depends(current_active_user)
                                ):
    global model, tokenizer
    conversation = await _service.get_conversation_by_id(conversation_id=conversation_id)
    
    if not conversation or current_user.id != conversation.user_id or request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Invalid request")
    query = request.messages[-1].content
    docs = vecDB.get_knowledge(query, top_k=request.top_k)
    query = str(resp_prompt.format_prompt(query=query, docs=docs))
    prev_messages = request.messages[:-1]
    if len(prev_messages) > 0 and prev_messages[0].role == "system":
        query = prev_messages.pop(0).content + query

    history = []
    if len(prev_messages) % 2 == 0:
        for i in range(0, len(prev_messages), 2):
            if prev_messages[i].role == "user" and prev_messages[i+1].role == "assistant":
                history.append([prev_messages[i].content,
                               prev_messages[i+1].content])

    if request.stream:
        generate = predict(query, history, request)
        return EventSourceResponse(generate, media_type="text/event-stream")

    response, _ = model.chat(tokenizer, query, history=history,
                             temperature=request.temperature, top_p=request.top_p, max_length=request.max_length)
    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=response),
        finish_reason="stop"
    )
    return ChatCompletionResponse(model=request.model, choices=[choice_data], object="chat.completion")


async def predict(query: str, history: List[List[str]], request: ChatCompletionRequest):
    global model, tokenizer

    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(role="assistant"),
        finish_reason=None
    )
    chunk = ChatCompletionResponse(model=request.model, choices=[
                                   choice_data], object="chat.completion.chunk")
    yield "{}".format(chunk.model_dump_json(exclude_unset=True, ensure_ascii=False))

    current_length = 0

    for new_response, _ in model.stream_chat(tokenizer, query, history=history, 
                                             temperature=request.temperature, top_p=request.top_p, max_length= request.max_length):
        if len(new_response) == current_length:
            continue

        new_text = new_response[current_length:]
        current_length = len(new_response)

        choice_data = ChatCompletionResponseStreamChoice(
            index=0,
            delta=DeltaMessage(content=new_text),
            finish_reason=None
        )
        chunk = ChatCompletionResponse(model=request.model, choices=[
                                       choice_data], object="chat.completion.chunk")
        yield "{}".format(chunk.model_dump_json(exclude_unset=True, ensure_ascii=False))
    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(),
        finish_reason="stop"
    )
    chunk = ChatCompletionResponse(model=request.model, choices=[
                                   choice_data], object="chat.completion.chunk")
    yield "{}".format(chunk.model_dump_json(exclude_unset=True, ensure_ascii=False))
    yield '[DONE]'

async def __predict(query: str, history: List[List[str]], model_id: str):
    global model, tokenizer

    current_length = 0

    for new_response, _ in model.stream_chat(tokenizer, query, history):
        if len(new_response) == current_length:
            continue
        new_text = new_response[current_length:]
        current_length = len(new_response)
        yield new_text
    yield '[DONE]'

async def local_chat(message: ChatMessage, messages: List[ChatMessage]):
    global model, tokenizer
    query = message.content
    docs = vecDB.get_knowledge(query)
    query = str(resp_prompt.format_prompt(query=query, docs=docs))
    prev_messages = messages[:-1]
    if len(prev_messages) > 0 and prev_messages[0].role == "system":
        query = prev_messages.pop(0).content + query

    history = []
    if len(prev_messages) % 2 == 0:
        for i in range(0, len(prev_messages), 2):
            if prev_messages[i].role == "user" and prev_messages[i+1].role == "assistant":
                history.append([prev_messages[i].content,
                               prev_messages[i+1].content])
    response = ''
    sys.stdout.write(f"Assistant: ")
    async for chunk in __predict(query, history, 'chatglm'):
        if chunk == '[DONE]':
            break
        sys.stdout.write(chunk)
        sys.stdout.flush()
        response += chunk
    print('\n')
    return response


if __name__ == "__main__":
    history = []
    while True:
        # 获取用户输入
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break
        query = ChatMessage(role='user', content=user_input)
        history.append(query)
        # 生成助手的回答
        response = asyncio.run(local_chat(query, history))

        # 更新对话历史
        history.append(ChatMessage(role='assistant', content=response))

    print("Goodbye!")
