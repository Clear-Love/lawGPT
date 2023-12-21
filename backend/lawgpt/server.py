"""server"""
import uvicorn
from fastapi import FastAPI
import lawgpt.middlewares
from lawgpt.config import settings
from lawgpt.log import init_log
from lawgpt.router import auth
from lawgpt.router import conv

class Server:

    def __init__(self):
        init_log()
        self.app = FastAPI()

    def init_app(self):
        lawgpt.middlewares.init_middleware(self.app)
        if settings.USE_OPENAI:
            from lawgpt.router.chatopenai import router
            self.app.router.include_router(
                router, prefix='/api', tags=['chat'])
        else:
            from lawgpt.router.chat import router
            self.app.router.include_router(
                router, prefix='/api', tags=['chat'])
        self.app.router.include_router(auth.router, prefix='/api/auth', tags=['auth'])
        self.app.router.include_router(
            conv.router, prefix='/api/conv', tags=['conversation'])

    def run(self):
        self.init_app()
        uvicorn.run(
            app=self.app,
            host=settings.HOST,
            port=settings.PORT,
        )

if __name__ == '__main__':
    Server().run()