import logging
import os
from shutil import copyfile

from dotenv import find_dotenv, load_dotenv
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))

# create .env file if it doesn't exist
app_root = os.path.dirname(os.path.dirname(__file__))
dotenv_path = os.path.join(app_root, '.env')

if not find_dotenv(dotenv_path) and os.getenv('DEV') == 'True':
    logger.info('Copying dev.env to .env')
    copyfile(os.path.join(app_root, 'dev.env'), dotenv_path)

load_dotenv(dotenv_path)

# read settings from env vars
WORKER_COUNT = int(os.getenv('WORKER_COUNT'))
DATABASE_URI = os.getenv('DATABASE_URI')
DATABASE_SCHEMA = os.getenv('DATABASE_SCHEMA')
DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW'))
DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE'))
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE'))

RABBIT_AMQP = os.getenv('RABBIT_AMQP')
RABBIT_INBOUND_QUEUE = os.getenv('RABBIT_INBOUND_QUEUE')
RABBIT_CASE_EVENT_EXCHANGE = os.getenv('RABBIT_CASE_EVENT_EXCHANGE')
RABBIT_CASE_EVENT_RH_QUEUE = os.getenv('RABBIT_CASE_EVENT_RH_QUEUE')
RABBIT_CASE_EVENT_ACTION_QUEUE = os.getenv('RABBIT_CASE_EVENT_ACTION_QUEUE')
