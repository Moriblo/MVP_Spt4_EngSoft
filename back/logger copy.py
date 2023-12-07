from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
import logging
import os


service_name = __name__
log_path = "log/"

# Verifica se o diretorio para anexar os logs não existe
if not os.path.exists(log_path):
    # Então cria o diretorio
    os.makedirs(log_path)

dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - call_trace=%(pathname)s L%(lineno)-4d",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        # "email": {
        #     "class": "logging.handlers.SMTPHandler",
        #     "formatter": "default",
        #     "level": "ERROR",
        #     "mailhost": ("smtp.example.com", 587),
        #     "fromaddr": "devops@example.com",
        #     "toaddrs": ["receiver@example.com", "receiver2@example.com"],
        #     "subject": "Error Logs",
        #     "credentials": ("username", "password"),
        # },
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "detailed",
            "filename": f"{log_path}/{service_name}.error.log",
            "when": "D", 
            "interval": 1, 
            "backupCount": 5
        },
        "detailed_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "detailed",
            "filename": f"{log_path}/{service_name}.detailed.log",
            "when": "D", 
            "interval": 1, 
            "backupCount": 5
        }
    },
    "loggers": {
        f"{service_name}.error": {
            "handlers": ["console", "error_file"],  #, email],
            "level": "DEBUG",
            "propagate": False,
        }
    },
    "root": {
        "handlers": ["console", "detailed_file"],
        "level": "DEBUG",
    }
})

logger = logging.getLogger(__name__)
