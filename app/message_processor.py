import json
import logging

import pika
from structlog import wrap_logger

from . import db, rabbit_utils, receivers, settings

logger = wrap_logger(logging.getLogger(__name__))


class MessageProcessor:
    def __init__(self, inbound_channel, outbound_channel):
        self.inbound_channel = inbound_channel
        self.outbound_channel = outbound_channel
        self._receiver_map = self._build_receiver_map()

    def __call__(self, inbound_channel, method, properties, body):
        try:
            with rabbit_utils.rabbit_transaction(self.inbound_channel, self.outbound_channel):
                with db.transaction() as self.session:
                    self.process_message(body)

                    inbound_channel.basic_ack(delivery_tag=method.delivery_tag)

        except:
            logger.error(
                'Exception thrown when processing message', exc_info=True)

            logger.info('Rejecting and requeuing inbound message')

            # reject and requeue the failed inbound message
            inbound_channel.basic_reject(
                delivery_tag=method.delivery_tag, requeue=True)
            # commit the reject
            inbound_channel.tx_commit()

    def process_message(self, body: str):
        """The callback method for inbound messages

        This method requires a receiver class to be defined which can handle the
        event type of this message
        """
        message = json.loads(body)
        receiver = self.get_receiver(message['type'])
        receiver.process_event(message)

    def emit_case_event(self, routing_key: str, message: dict):
        self.outbound_channel.basic_publish(
            settings.RABBIT_CASE_EVENT_EXCHANGE,
            routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=1),
            mandatory=True)

    def _build_receiver_map(self):
        """Gets all of the receiver classes and instatiates them
        """
        return {
            cls.get_event_type(): cls(self)
            for cls in receivers.BaseReceiver.__subclasses__()
        }

    def get_receiver(self, event_type: str):
        if event_type not in self._receiver_map:
            raise Exception(f'No receiver found for event type "{event_type}"')

        return self._receiver_map[event_type]
