import os
import logging
from dotenv import load_dotenv

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(APP_DIR))
ENV_DIR = os.path.join(PROJECT_DIR, 'env')


if os.path.exists(os.path.join(ENV_DIR, '.env')):
    load_dotenv(os.path.join(ENV_DIR, '.env'))

try:
    LEDGER = os.getenv('LEDGER')
except NameError as e:
    print(e)

LOG_LEVEL = os.environ.setdefault('LOG_LEVEL', 'NOTSET')


def get_log_level():
    """Return the current **LOG_LEVEL** in the settings as a string.

    :return: The log level
    :rtype: str
    """
    if LOG_LEVEL == 'INFO':
        return logging.INFO
    if LOG_LEVEL == 'DEBUG':
        return logging.DEBUG
    if LOG_LEVEL == 'ERROR':
        return logging.ERROR
    return logging.NOTSET
