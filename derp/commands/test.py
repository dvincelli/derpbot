import random
import time
import re
import logging


logger = logging.getLogger(__name__)


class EchoCommand(object):
    command = 'echo'

    def parse(self, body):
        return ' '.join(body.split(' ')[1:])

    def __call__(self, msg):
        return self.parse(msg['body'])


class PingCommand(object):
    command = 'ping'

    def __call__(self, msg):
        return 'pong'
