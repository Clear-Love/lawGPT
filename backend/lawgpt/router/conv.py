import asyncio
from typing import List
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from lawgpt.log import get_logger
from lawgpt.models.dbModels import User
from lawgpt.models.reqModels import ContentSchema, ConversationSchema, CreateContentRequest, CreateContentSchema, CreateConversationRequset, CreateConversationSchema
from lawgpt.models.respModels import ConversationHistory
from lawgpt.response import response
from lawgpt.services.chatService import ChatService
from lawgpt.utils.user_manager import current_active_user


router = APIRouter()
logger = get_logger(__name__)
_service = ChatService()


async def checkConversation(conversation_id: str, current_user: User) -> ConversationSchema:
    conversation = await _service.get_conversation_by_id(conversation_id=conversation_id)
    if not conversation or current_user.id != conversation.user_id:
        raise HTTPException(status_code=502, detail="Invalid request")
    return conversation

@router.post('/new', response_model=ConversationSchema, description="新建对话")
async def new_conversation(request: CreateConversationRequset, current_user: User = Depends(current_active_user)):
    try:
        converaation = await _service.new_conversation(CreateConversationSchema(id= str(uuid4()), title=request.title, user_id=current_user.id))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return converaation

@router.get('/conversation', response_model=List[ConversationSchema], description="获取所有对话")
async def get_conversation(current_user: User = Depends(current_active_user)):
    conversations = await _service.get_all_conversation(current_user.id)
    return conversations


@router.get('/messages/{conversation_id}', response_model=ConversationHistory, description="获取所有对话")
async def get_messages(conversation_id: str, current_user: User = Depends(current_active_user)):
    t1 = checkConversation(conversation_id, current_user)
    t2 = _service.get_all_content(conversation_id)
    conversation, messages = await asyncio.gather(t1, t2)
    return createConversationHistory(conversation, messages)


@router.post('/newmessage/{conversation_id}', response_model=ContentSchema, description="新建对话")
async def get_messages(conversation_id: str, request: CreateContentRequest, current_user: User = Depends(current_active_user)):
    await checkConversation(conversation_id, current_user)
    content = await _service.save_content(CreateContentSchema(id= str(uuid4()), role=request.role, content=request.content, conversation_id=conversation_id))
    return content


@router.post('/delete/{conversation_id}', description="删除对话")
async def delete_conversation(conversation_id: str, current_user: User = Depends(current_active_user)):
    conversation = await checkConversation(conversation_id, current_user)
    await _service.delete_conversation(conversation)
    return response(message="success")


@router.post('/clear/{conversation_id}', description="删除对话")
async def delete_conversation(conversation_id: str, current_user: User = Depends(current_active_user)):
    conversation = await checkConversation(conversation_id, current_user)
    await _service.delete_history(conversation)
    return response(message="success")

def createConversationHistory(conversation: ConversationSchema, messages: List[ContentSchema]) -> ConversationHistory:
    logger.info(conversation)
    logger.info(conversation.curr_content)
    res = ConversationHistory(conversation_id=conversation.id, curr_node=conversation.curr_content, messages={})
    for msg in messages:
        res.messages[msg.id] = msg
    return res

