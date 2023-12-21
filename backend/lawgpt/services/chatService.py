from typing import List, Optional
from MySQLdb import IntegrityError
from fastapi import HTTPException

from sqlalchemy import delete, select
from lawgpt.log import get_logger
from lawgpt.models.dbModels import Content
from lawgpt.models.reqModels import ContentSchema, ConversationSchema, CreateContentSchema, \
    CreateConversationSchema
from lawgpt.models.dbModels import Conversation
from lawgpt.db import get_async_session_context

logger = get_logger(__name__)

class ChatService:

    async def save_content(self, create_content: CreateContentSchema) -> Content:
        logger.info(create_content.id)
        content = create_content.model_dump()
        async with get_async_session_context() as session:
            conversation = await session.get(Conversation, create_content.conversation_id)
            if conversation.curr_content:
                content['parent'] = conversation.curr_content
            content = Content(**content)
            conversation.curr_content = content.id
            session.add(content)
            session.add(conversation)
            await session.commit()
            await session.refresh(content)
            await session.refresh(conversation)
            return content

    async def get_all_conversation(self, user_id: int) -> List[ConversationSchema]:
        async with get_async_session_context() as session:
            r = await session.execute(select(Conversation).filter(Conversation.user_id == user_id))
            result = r.scalars().all()
            return result

    async def get_all_content(self, conversation_id: str) -> List[ContentSchema]:
        async with get_async_session_context() as session:
            r = await session.execute(select(Content).filter(Content.conversation_id == conversation_id))
            result = r.scalars().all()
            return result

    async def get_conversation_by_id(self, conversation_id: str) -> ConversationSchema:
        async with get_async_session_context() as session:
            conversation = await session.get(Conversation, conversation_id)
            return conversation

    async def new_conversation(self, create_conversation: CreateConversationSchema) -> Conversation:
        conversation = Conversation(**create_conversation.model_dump())
        async with get_async_session_context() as session:
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation
    
    async def delete_history(self, conversation: Conversation):
        async with get_async_session_context() as session:
            try:
                # 删除conversation及其所有content
                await session.execute(
                    delete(Content).where(Content.conversation_id == conversation.id))
                await session.commit()
            except Exception as e:
                logger.error(e)
                session.rollback()
                raise HTTPException(status_code=500, detail="内部错误")
    
    async def delete_conversation(self, conversation: Conversation):
        async with get_async_session_context() as session:
            try:
                # 删除conversation及其所有content
                await session.execute(
                    delete(Content).where(Content.conversation_id == conversation.id))
                await session.execute(
                    delete(Conversation).where(Conversation.id == conversation.id))
                await session.commit()
            except Exception as e:
                logger.error(e)
                session.rollback()
                raise HTTPException(status_code=500, detail="内部错误")

    async def set_title(self, conversation_id: str, user_id: int, title: str):
        logger.info(title)
        async with get_async_session_context() as session:
            try:
                conversation = await session.get(Conversation, conversation_id)
                if user_id != conversation.user_id:
                    raise HTTPException(status_code=501, detail="非法请求")
                conversation.title = title
                await session.commit()
                await session.refresh(conversation)
            except Exception as e:
                logger.error(e)
                session.rollback()
                raise HTTPException(status_code=500, detail="内部错误")
