import re

class BombCommand(object):
    pattern = re.compile('(\d+) (![^\s]+)(.*)')

    message_queue = 'message_queue'

    def parse(self, msg):
        return self.pattern.match(msg['body']).groups()

    def __call__(self, msg):
        repeats, command, etc = self.parse(msg)
        msg['body'] = command + etc
        for x in xrange(0, min(int(repeats), 50)):
            self.message_queue.put(msg)
