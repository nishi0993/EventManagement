import environ
import os
from boto3.session import Session

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()

WATCHTOWER_ENABLED = env("WATCHTOWER_ENABLED", default=False)
LOG_LEVEL = env("LOG_LEVEL", default="INFO")

if WATCHTOWER_ENABLED:
    CLOUDWATCH_AWS_ID = env('AWS_CLOUDWATCH_ID', default="")
    CLOUDWATCH_AWS_KEY = env('AWS_CLOUDWATCH_KEY', default="")
    AWS_DEFAULT_REGION = 'ap-south-1' # Be sure to update with your AWS region
    logger_boto3_session = Session(
        aws_access_key_id=CLOUDWATCH_AWS_ID,
        aws_secret_access_key=CLOUDWATCH_AWS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
        },
        "formatters": {
            "aws": {
                "format": "%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
                "datefmt": "%d-%m-%Y %H:%M:%S",
            },
        },
        "handlers": {
            "watchtower": {
                "level": LOG_LEVEL,
                "class": "watchtower.CloudWatchLogHandler",
                # From step 2
                "boto3_session": logger_boto3_session,
                "log_group": "DatahackLogs",
                # Different stream for each environment
                "stream_name": f"applications logs",
                "formatter": "aws",
            },
            "console": {"class": "logging.StreamHandler", "formatter": "aws",},
            "file": {
                "class": "logging.FileHandler",
                "filename": "debug.log",
                "formatter": "aws"
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": ["watchtower", "file", "mail_admins"], "propogate": False,}
        },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
        },
        "formatters": {
            "aws": {
                "format": "%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "aws"},
            "file": {
                "class": "logging.FileHandler",
                "filename": "debug.log",
                "formatter": "aws"
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": ["file", "console", "mail_admins"], "propogate": False}
        },
    }
