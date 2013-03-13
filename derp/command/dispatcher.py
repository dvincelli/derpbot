import multiprocessing
import logging
import re

multiprocessing.log_to_stderr(logging.DEBUG)

class CommandDispatcher(object):

    pool = multiprocessing.Pool()

    bomb_pattern = re.compile('(\d+) (![^\s]+)(.*)')

    def __init__(self, message_processor, message_responder):
        self.message_processor = message_processor
        self.message_responder = message_responder

    def put(self, message):
        args = tuple([
            message['type'],
            message['from'].bare,
            message['to'].bare,
            message['body'],
            message['status']
        ])
        self.pool.apply_async(
            self.message_processor,
            args,
            callback=self.message_responder
        )

    def is_bomb(self, message):
        return self.bomb_pattern.match(message['body'])

    def parse_bomb(self, message):
        return self.bomb_pattern.match(message['body']).groups()

    def __call__(self, message):
        repeats = 1
        if self.is_bomb(message):
            repeats, command, etc = self.parse_bomb(message)
            message['body'] = command + etc
            repeats = min(int(repeats), 50)
        for x in xrange(0, repeats):
            self.put(message)

