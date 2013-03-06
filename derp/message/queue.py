import multiprocessing

class MessageQueue(object):

    pool = multiprocessing.Pool()

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

    def __call__(self, message):
        return self.put(message)

