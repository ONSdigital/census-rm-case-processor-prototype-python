import functools
import json
import logging
from contextlib import contextmanager

import pika
from pika.exceptions import AMQPError
from sqlalchemy.exc import SQLAlchemyError
from structlog import wrap_logger

from . import message_processor, rabbit_utils, settings

logger = wrap_logger(logging.getLogger(__name__))


def start_worker():
    logger.info(f'Starting inbound queue worker')

    # pika connections are not threadsafe so this is created within the worker
    connection = pika.BlockingConnection(
        pika.URLParameters(settings.RABBIT_AMQP))

    while True:
        inbound_channel = rabbit_utils.init_inbound_channel(connection)
        outbound_channel = rabbit_utils.init_outbound_channel(connection)
        logger.info('Consuming...')

        processor = message_processor.MessageProcessor(inbound_channel, outbound_channel)
        inbound_channel.basic_consume(
            settings.RABBIT_INBOUND_QUEUE, on_message_callback=processor)

        try:
            inbound_channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            logger.info('Connection closed. Recovering')
            continue
        except KeyboardInterrupt:
            inbound_channel.stop_consuming()
        finally:
            connection.close()
            break
