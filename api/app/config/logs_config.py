import logging
import logging.config
from app.config.email_handler import EmailHandler
from app.config.configs import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "mode": "a",
        },
        "email": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "app.config.email_handler.EmailHandler",
            "mailhost": ("smtp.example.com", 587),
            "fromaddr": "your_email@example.com",
            "toaddrs": [settings.EMAIL_SEND_LOG_01, settings.EMAIL_SEND_LOG_02],
            "subject": "Error Log",
            "credentials": (settings.EMAIL_lOG, settings.PASSWORD_LOG),
            "secure": None
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default", "file", "email"],
            "level": "INFO",
            "propagate": True
        },
        "uvicorn.error": {
            "handlers": ["default", "file", "email"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
