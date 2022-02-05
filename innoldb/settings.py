import os
import logging
from dotenv import load_dotenv

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
ENV_DIR = os.path.join(PROJECT_DIR,'env')


if os.path.exists(os.path.join(ENV_DIR, '.env')):
  load_dotenv(os.path.join(ENV_DIR, '.env'))

LEDGER = os.environ.setdefault('LEDGER', 'laboratory')
DEFAULT_INDEX = os.environ.setdefault('DEFAULT_INDEX', 'id')

LOG_LEVEL = os.environ.setdefault('LOG_LEVEL', None)

def get_log_level():
  if LOG_LEVEL == 'INFO':
    return logging.INFO
  if LOG_LEVEL == 'DEBUG':
    return logging.DEBUG
  if LOG_LEVEL == 'ERROR':
    return logging.ERROR
  return logging.NOTSET