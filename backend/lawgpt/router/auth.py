import random
from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.authentication import Strategy
from sqlalchemy.future import select
from starlette.requests import Request

from lawgpt.models.respModels import CreateUserRequest, resetPasswordRequest
from lawgpt.services.emailService import EmailSender
from lawgpt.services.redisService import RedisClient
from lawgpt.exceptions import AuthenticationFailedException
from lawgpt.log import get_logger
from lawgpt.models.dbModels import User
from lawgpt.models.reqModels import CreateUserSchema, ReadUserSchema, UpdateUserSchema, validEmailRequest
from lawgpt.response import response
from lawgpt.utils.user_manager import UserManager, auth_backend, current_active_user, current_super_user, get_by_email, get_by_username_or_email, get_user_manager, \
    get_current_user_token, get_async_session_context, get_user_db_context, get_user_manager_context

router = APIRouter()
logger = get_logger(__name__)
redis = RedisClient()
emailsender = EmailSender()

@router.post("/login", name=f"auth:{auth_backend.name}.login")
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: UserManager = Depends(get_user_manager),
        strategy: Strategy[User, int] = Depends(auth_backend.get_strategy),
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise AuthenticationFailedException()
    resp = await auth_backend.login(strategy, user)
    return response(200, headers=resp.headers)


@router.post("/logout", name=f"auth:{auth_backend.name}.logout")
async def logout(
        user_token: Tuple[User, str] = Depends(get_current_user_token),
        strategy: Strategy[User, int] = Depends(auth_backend.get_strategy),
):
    user, token = user_token
    logger.info(token)
    resp = await auth_backend.logout(strategy, user, token)
    return response(200, headers=resp.headers)


@router.get("/user", tags=["user"])
async def get_all_users(_: User = Depends(current_super_user)):
    async with get_async_session_context() as session:
        r = await session.execute(select(User))
        results = r.scalars().all()
        return results


@router.get("/user/me", response_model=ReadUserSchema, tags=["user"])
async def get_me(user: User = Depends(current_active_user)):
    return user


@router.patch("/user/me", response_model=ReadUserSchema, tags=["user"])
async def update_me(
        request: Request,
        user_update: UpdateUserSchema,  # type: ignore
        _user: User = Depends(current_active_user),
):
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.update(
                    user_update, _user, safe=True, request=request
                )
                return user


@router.delete("/user/{user_id}", tags=["user"])
async def admin_delete_user(user_id: int, _: User = Depends(current_super_user)):
    async with get_async_session_context() as session:
        user = await session.get(User, user_id)
        await session.delete(user)
        await session.commit()
        return None

@router.post('/sendValidEmail')
async def sendValidEmail(request: validEmailRequest):
    email = request.email
    key = 'email' + email + 'valid'
    if redis.ttl(key) > 120:
        raise HTTPException(status_code=429, detail="请求频繁，请稍后再试")
    user = await get_by_email(email)
    if user:
        raise HTTPException(status_code=502, detail="该邮箱已被注册")
    code = random.randint(100000, 999999)
    try:
        emailsender.send_email(email, "验证邮件", f"验证码是：{code}")
        redis.set(key, str(code), 180)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="邮件发送失败，请检查邮件地址是否有效")
    return response(message='发送成功')


@router.post('/sendResetEmail')
async def sendResetEmail(request: validEmailRequest):
    email = request.email
    key = 'email' + email + 'reset'
    if redis.ttl(key) > 120:
        raise HTTPException(status_code=429, detail="请求频繁，请稍后再试")
    user = await get_by_email(email)
    if not user:
        raise HTTPException(status_code=502, detail="没有该邮箱的账户")
    code = random.randint(100000, 999999)
    try:
        emailsender.send_email(email, "验证邮件", f"验证码是：{code}")
        redis.set(key, str(code), 180)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="邮件发送失败，请检查邮件地址是否有效")
    return response(message='发送成功')


@router.post("/register", response_model=ReadUserSchema, tags=["auth"])
async def register(
        user_create: CreateUserRequest,
):
    user = await get_by_username_or_email(user_create.username)
    if user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    key = 'email' + user_create.email + 'valid'
    code = redis.get_str(key)
    logger.info(code + " and " + user_create.code)
    if not code:
        raise HTTPException(status_code=400, detail="验证码失效，请重新发送")
    if code != user_create.code:
        raise HTTPException(status_code=400, detail="验证码错误，请重新检查后再提交")
    userCreate = CreateUserSchema(
        username=user_create.username,
        nickname=user_create.username,
        email=user_create.email,
        avatar="",
        password=user_create.password
    )
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(userCreate, safe=False)
                return user


@router.post("/reset", response_model=ReadUserSchema, tags=["auth"])
async def resetPassword(
        user_update: resetPasswordRequest,
):
    user = await get_by_email(user_update.email)
    if not user:
        raise HTTPException(status_code=400, detail="该用户不存在")
    key = 'email' + user_update.email + 'reset'
    code = redis.get_str(key)
    if not code:
        raise HTTPException(status_code=400, detail="验证码失效，请重新发送")
    if code != user_update.code:
        raise HTTPException(status_code=400, detail="验证码错误，请重新检查后再提交")
    userUpdate = UpdateUserSchema(
        password=user_update.password
    )
    userUpdate.password = user_update.password
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.update(userUpdate, user)
                return user