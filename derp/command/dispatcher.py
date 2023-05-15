import multiprocessing
import queue
import logging
import re
import os


logger = logging.getLogger(__name__)


class CommandDispatcher:
    message_processing_backend = 'sync'

    def __init__(self, message_processor, message_responder):
        self.message_processor = message_processor
        self.message_responder = message_responder
        if self.message_processing_backend == 'multiprocessing':
            multiprocessing.log_to_stderr(logging.DEBUG)
            self.pool = multiprocessing.Pool()

    def put(self, message):
        if self.message_processing_backend == 'multiprocessing':
            self.pool.apply_async(
                self.message_processor, message, callback=self.message_responder
            )
        else:
            response = self.message_processor(message)
            logger.debug('response %r', response)
            return self.message_responder(response)

    def __call__(self, client, req):
        try:
            logger.info('req %r', req)
            slack_message = req.to_dict()['payload']['event']
            logger.debug('slack_message %r', slack_message)

            if slack_message.get('subtype') == 'bot_message':
                logger.debug('Ignored, subtype is botmessage ...')
                # ignore ourself
                return

            message = {}
            message["body"] = slack_message["text"]
            message["to"] = slack_message["user"]
            message["from"] = slack_message["channel"]

            self.put(message)

        except KeyError as e:
            logger.exception("%s while handling message", e)
            return

