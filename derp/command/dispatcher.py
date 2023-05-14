import multiprocessing
import queue
import logging
import re
import os


logger = logging.getLogger(__name__)


class CommandDispatcher:
    #__name__ = "derp_bot"

    message_processing_backend = os.getenv('MESSAGE_PROCESSING_BACKEND', 'sync')

    bomb_pattern = re.compile("(\d+) (![^\s]+)(.*)")

    def __init__(self, message_processor, message_responder):
        self.message_processor = message_processor
        self.message_responder = message_responder
        if self.message_processing_backend == 'multiprocessing':
            multiprocessing.log_to_stderr(logging.DEBUG)
            self.pool = multiprocessing.Pool()

    def put(self, message):
        args = tuple(
            [
                message["from"],
                message["to"],
                message["body"],
            ]
        )
        if self.message_processing_backend == 'multiprocessing':
            self.pool.apply_async(
                self.message_processor, args, callback=self.message_responder
            )
        else:
            response = self.message_processor(*args)
            logger.debug('response %r', response)
            return self.message_responder(response)

    def is_bomb(self, message):
        return self.bomb_pattern.match(message["body"])

    def parse_bomb(self, message):
        return self.bomb_pattern.match(message["body"]).groups()

    def __call__(self, client, req):
        try:
            logger.info('req %r', req)
            slack_message = req.to_dict()['payload']['event']
            logger.debug('slack_message %r', slack_message)

            if slack_message.get('subtype') == 'bot_message':
                # ignore ourself
                return

            message = {}
            message["body"] = slack_message["text"]
            message["to"] = slack_message["user"]
            message["from"] = slack_message["channel"]

            logger.debug('reply message: %r', message)
        except KeyError:
            logger.exception("KeyError handling slack_message %r", slack_message)
            return

        repeats = 1
        if self.is_bomb(message):
            repeats, command, etc = self.parse_bomb(message)
            message["body"] = command + etc
            repeats = min(int(repeats), 50)
        for x in range(0, repeats):
            self.put(message)
