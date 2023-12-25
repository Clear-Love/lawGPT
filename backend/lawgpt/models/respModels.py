from datetime import datetime
import time
from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

from lawgpt.models.reqModels import ChatMessage, ContentSchema, DeltaMessage


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]]


class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[Union[ChatCompletionResponseChoice,
                        ChatCompletionResponseStreamChoice]]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))

class SearchResponse(BaseModel):
    docs: List[str]

class ConversationHistory(BaseModel):
    conversation_id: str
    messages: Dict[str, ContentSchema]
    curr_node: Union[str, None]

class GenTitleRequest(BaseModel):
    title: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    code: str


class resetPasswordRequest(BaseModel):
    password: str
    email: str
    code: str