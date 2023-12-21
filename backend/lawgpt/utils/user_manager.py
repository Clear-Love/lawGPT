import contextlib
import re
from datetime import datetime, timezone
from typing import Any, Optional
from lawgpt.db import get_async_session_context, get_user_db, get_user_db_context
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, FastAPIUsers, models, IntegerIDMixin, InvalidID
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users.models import UP
from sqlalchemy import or_, select, Integer
from starlette.websockets import WebSocket
from lawgpt.config import settings
from lawgpt.log import get_logger
from lawgpt.models.dbModels import User
import lawgpt.exceptions as exceptions
from lawgpt.models.reqModels import CreateUserSchema, UpdateUserSchema


logger = get_logger(__name__)

# 使用 cookie + JWT
# 参考 https://fastapi-users.github.io/fastapi-users/10.2/configuration/full-example/

COOKIE_NAME = "token"

cookie_transport = CookieTransport(
    cookie_max_age=settings.AUTH.COOKIE_MAX_AGE,
    cookie_name=COOKIE_NAME,
    cookie_httponly=False,
    cookie_secure=False,
)


# auth backend

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.AUTH.JWT_SECRET,
                       lifetime_seconds=settings.AUTH.JWT_LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# UserManager

SECRET = settings.AUTH.USER_SECRET


async def get_by_username_or_email(text: str) -> Optional[UP]:
    async with get_async_session_context() as session:
        user = await session.execute(select(User).where(or_(User.username == text, User.email == text)))
        user = user.scalar_one_or_none()
        if not user:
            return None
        return user


async def get_by_email(email: str) -> Optional[User]:
    async with get_async_session_context() as session:
        user = await session.execute(select(User).filter(User.email == email))
        user = user.scalar_one_or_none()
        if not user:
            return None
        return user


class UserManager(IntegerIDMixin, BaseUserManager[User, Integer]):

    async def validate_password(self, password: str, user: Any) -> None:
        if len(password) < 6:
            raise exceptions.InvalidParamsException("Password too short")
        if len(password) > 32:
            raise exceptions.InvalidParamsException("Password too long")
        # 用正则检查：仅包含数字、字母和符号（\w!@#$%^&*()_+|{}:;<>?~`-），不含空格
        if not re.match(r"^[\w!@#$%^&*()_+|{}:;<>?~`-]+$", password):
            raise exceptions.InvalidParamsException(
                "Password contains invalid characters")
        return

    async def _check_username_unique(self, username, exclude_username=None):
        if not username:
            return
        async with get_async_session_context() as session:
            user = (await session.execute(select(User).filter(User.username == username))).scalar_one_or_none()
            if user and user.username != exclude_username:
                raise exceptions.UserAlreadyExists(
                    "Username already exists")
            # TODO 暂时没有检查email是否unique

    async def create(self, user_create: CreateUserSchema, safe: bool = False) -> User:
        if (len(user_create.username) < 4 or len(user_create.username) > 12):
            raise exceptions.UserAlreadyExists(
                "用户名长度应为4-12位")
        await self._check_username_unique(username=user_create.username)
        await self.validate_password(user_create.password, user_create)

        user_dict = user_create.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["is_active"] = True
        user_dict["is_superuser"] = False
        user_dict["is_verified"] = False
        user = User(**user_dict)
        async with get_async_session_context() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update(self, user_update: UpdateUserSchema, user: User,safe: bool = False) -> User:
        update_dict = user_update.model_dump(exclude_unset=True)
        if "password" in update_dict:
            await self.validate_password(user_update.password, user_update)
            update_dict["hashed_password"] = self.password_helper.hash(
                update_dict.pop("password"))
        if "username" in update_dict:
            await self._check_username_unique(username=update_dict["username"], exclude_username=user.username)
        if safe:
            try:
                update_dict.pop("is_active")
                update_dict.pop("is_superuser")
                update_dict.pop("is_verified")
            except KeyError:
                pass
        async with get_async_session_context() as session:
            user = await session.get(User, user.id)
            if not user:
                raise exceptions.UserNotExistException(
                    "user not find"
                )
            for key, value in update_dict.items():
                setattr(user, key, value)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def parse_id(self, value: Any) -> int:
        try:
            return int(value)
        except ValueError as e:
            raise InvalidID() from e

    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.
        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        user = await get_by_username_or_email(credentials.username)

        if user is None:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


async def websocket_auth(websocket: WebSocket) -> User | None:
    user_db = None
    try:
        cookie = websocket._cookies[COOKIE_NAME]
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    # user = await get_jwt_strategy().read_token(cookie, user_manager)
                    user_db, _ = await fastapi_users.authenticator._authenticate(
                        active=True,
                        user_manager=user_manager,
                        jwt=cookie,
                        strategy_jwt=get_jwt_strategy(),
                    )
    finally:
        return user_db


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

# FastAPIUsers 实例，注意不要和 fastapi_users 包混淆
fastapi_users = FastAPIUsers[User, Integer](get_user_manager, [auth_backend])

__current_active_user = fastapi_users.current_user(active=True)


async def current_active_user(request: Request, user: User = Depends(__current_active_user)):
    try:
        async with get_async_session_context() as session:
            user_update = await session.get(User, user.id)
            user_update.last_active_time = datetime.now().astimezone(tz=timezone.utc)
            session.add(user_update)
            await session.commit()
        request.scope["auth_user"] = user
    except Exception as e:
        raise e
    finally:
        return user


# current_super_user = fastapi_users.current_user(active=True, superuser=True)

async def current_super_user(user: User = Depends(current_active_user)):
    if not user.is_superuser:
        raise exceptions.AuthorityDenyException("You are not super user")
    return user

get_current_user_token = fastapi_users.authenticator.current_user_token(
    active=True, verified=False
)