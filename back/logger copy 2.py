import logging
import os
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from datetime import datetime

def configure_logger(service_name, log_path):

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    if service_name =="" or service_name is None or log_path =="" or log_path is None:
        service_name = __name__
        log_path = "log/"
    
    hora_formatada = datetime.now().strftime("%H:%M:%S")[:8].replace(":", "")
    service_name = service_name + hora_formatada

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

    logger = logging.getLogger(service_name)
    return logger
