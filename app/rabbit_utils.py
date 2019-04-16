import logging
from contextlib import contextmanager

from structlog import wrap_logger

from . import settings

logger = wrap_logger(logging.getLogger(__name__))


@contextmanager
def rabbit_transaction(*all_channels):
    """Runs a commit or a rollback on both inbound and outbound channels
    """
    try:
        yield
    except:
        logger.info('Rolling back rabbit transaction')

        for channel in all_channels:
            channel.tx_rollback()
        raise
    else:
        for channel in all_channels:
            channel.tx_commit()


def init_inbound_channel(connection):
    """Create and configure the channel to receive inbound messages
    """
    channel = connection.channel()
    channel.basic_qos(prefetch_count=100)
    channel.queue_declare(
        queue=settings.RABBIT_INBOUND_QUEUE, durable=True)
    channel.tx_select()

    return channel


def init_outbound_channel(connection):
    """Create and configure the channel to publish messages
    """
    channel = connection.channel()
    channel.exchange_declare(
        settings.RABBIT_CASE_EVENT_EXCHANGE, exchange_type='fanout', durable=True)

    fanout_queues = (
        settings.RABBIT_CASE_EVENT_RH_QUEUE,
        settings.RABBIT_CASE_EVENT_ACTION_QUEUE,
    )
    for queue in fanout_queues:
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(queue, settings.RABBIT_CASE_EVENT_EXCHANGE)

    channel.tx_select()

    return channel
