import os
from dotenv import load_dotenv

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(APP_DIR)
ENV_DIR = os.path.join(PROJECT_DIR,'env')

if os.path.exists(os.path.join(ENV_DIR, '.env')):
  load_dotenv(os.path.join(ENV_DIR, '.env'))

LEDGER = os.environ.setdefault('LEDGER', 'innolab-qldb')