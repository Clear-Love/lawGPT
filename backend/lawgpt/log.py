import logging
from logging.config import dictConfig

from lawgpt.config import settings


def init_log():
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'sample': {'format': '%(asctime)s %(levelname)s %(message)s'},
            'verbose': {'format': '%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s'},
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            },
        },
        'handlers': {
            "console": {
                "formatter": 'verbose',
                'level': 'DEBUG',
                "class": "logging.StreamHandler",
            },
        },
        'loggers': {
            '': {'level': settings.LOG_LEVEL, 'handlers': ['console']},
        },
    }

    dictConfig(log_config)


def get_logger(name):
    return logging.getLogger(f"lawGPT.{name}")
