from datetime import datetime, timedelta
import string
from typing import List, Literal, Optional, TypeVar, Union
from unittest.mock import Base
from uuid import uuid4
from pydantic import BaseModel

from lawgpt.models.dbModels import BaseModel as DBModel

ModelType = TypeVar('ModelType', bound=DBModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class InDBMixin(BaseModel):
    class Config:
        from_attributes = True

# 用户
class BaseUser(InDBMixin):
    username: str
    nickname: Union[str, None]
    email: str
    avatar: Union[str, None]

class UserSchema(BaseUser):
    hashed_password: str
    last_active_time: datetime
    create_time: datetime
    is_superuser: bool
    is_verified: bool
    is_active: bool
    id: int

class ReadUserSchema(BaseUser):
    last_active_time: datetime
    create_time: datetime
    is_superuser: bool
    is_verified: bool
    is_active: bool
    id: int

class CreateUserSchema(BaseUser):
    password: str


class UpdateUserSchema(BaseModel):
    username: Union[str, None] = None
    nickname: Union[str, None] = None
    email: Union[str, None] = None
    avatar: Union[str, None] = None
    password: Union[str, None] = None
    last_active_time: Union[datetime, None] = None
    create_time: Union[datetime, None] = None

# 对话
class BaseConversation(InDBMixin):
    title: Optional[str]
    type: Literal["chat", "search"]


class ConversationSchema(BaseConversation):
    id: str
    user_id: int
    curr_content: Union[str, None]
    create_time: datetime
    update_time: datetime

class CreateConversationSchema(BaseConversation):
    id: str = uuid4()
    user_id: int
    curr_content: str = None

class CreateConversationRequset(BaseModel):
    title: str
    type: Literal["chat", "search"]


class UpdateConversationSchema(BaseConversation):
    pass


# 对话上下文
class BaseContent(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ContentSchema(BaseContent, InDBMixin):
    id: str
    parent: Union[str, None]
    conversation_id: str
    create_time: Union[datetime, None]


class CreateContentSchema(BaseContent):
    id: str
    conversation_id: str

class UpdateContentSchema(BaseContent):
    pass

class CreateContentRequest(BaseContent):
    pass


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1
    top_k: Optional[int] = 4
    max_length: Optional[int] = 2140
    stream: Optional[bool] = False

class validEmailRequest(BaseModel):
    email: str

class updateTitleRequest(BaseModel):
    history: str