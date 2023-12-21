from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Mapped, mapped_column

from lawgpt.utils.utc_datetime import UTCDateTime


class CustomBase:
    """https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html"""

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_collate': 'utf8mb4_general_ci'
    }


BaseModel = declarative_base(cls=CustomBase)


class Content(BaseModel):
    __tablename__ = 'content'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, comment='id')
    conversation_id: Mapped[str] = mapped_column(String(255), ForeignKey('conversation.id'), nullable=False, comment='所属对话id')
    content: Mapped[str] = mapped_column(Text, nullable=False, comment='问题')
    create_time: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(timezone=True), server_default=func.now(), comment="创建时间")
    role: Mapped[str] = mapped_column(Enum('system', 'user', 'assistant'), nullable=False, comment='回答')
    parent: Mapped[str] = mapped_column(String(255), nullable=True, comment='父节点')
 

class User(BaseModel):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True, nullable=False, comment='用户id')
    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment='用户名')
    nickname: Mapped[str] = mapped_column(String(32), nullable=False, comment='昵称')
    last_active_time: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(timezone=True), server_default=func.now(), comment="最后活跃时间")
    create_time: Mapped[datetime] = mapped_column(UTCDateTime(timezone=True), server_default=func.now(), comment="创建时间")
    avatar: Mapped[Optional[str]] = mapped_column(comment="头像")
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False, comment='密码')
    is_superuser: Mapped[bool] = mapped_column(Boolean, comment="是否是管理员")
    is_verified: Mapped[bool] = mapped_column(Boolean, comment="是否已经验证")
    is_active: Mapped[bool] = mapped_column(Boolean, comment="启用/禁用用户")
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, comment='邮箱')


class Conversation(BaseModel):
    __tablename__ = 'conversation'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, comment='对话id')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment='所属用户id')
    title: Mapped[str] = mapped_column(String(255), nullable=True, comment='标题')
    curr_content: Mapped[str] = mapped_column(String(255), nullable=True, comment="当前对话尾部节点")
    create_time: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(timezone=True), server_default=func.now(), comment="最后更新时间")