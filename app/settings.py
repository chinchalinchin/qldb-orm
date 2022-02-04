import os
from dotenv import load_dotenv

if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')):
  load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

LEDGER = os.environ.setdefault('LEDGER', 'innolab-qldb')