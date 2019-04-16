import logging
import os
import threading
import time

from structlog import wrap_logger

from app import db, settings, worker
from app.app_logging import logger_initial_config

logger = wrap_logger(logging.getLogger(__name__))


def main():
    """
    Main entry point of the subscriber worker
    """
    logger_initial_config(service_name="census-rm-case-service",
                          log_level=os.getenv("LOG_LEVEL", "INFO"))

    db.initialise_db()

    start_workers()


def start_workers():
    worker_count = settings.WORKER_COUNT
    logger.info(f'Starting {worker_count} worker threads')

    workers = []
    for _ in range(0, worker_count):
        worker_thread = threading.Thread(
            target=worker.start_worker, daemon=False)
        workers.append(worker_thread)
        worker_thread.start()

    logger.info(f'Workers started')


if __name__ == '__main__':
    main()
