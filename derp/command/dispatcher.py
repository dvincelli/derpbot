import multiprocessing
import logging
import re


multiprocessing.log_to_stderr(logging.INFO)


class CommandDispatcher(object):
    __name__ = 'derp_bot'

    pool = multiprocessing.Pool()

    bomb_pattern = re.compile('(\d+) (![^\s]+)(.*)')

    def __init__(self, message_processor, message_responder):
        self.message_processor = message_processor
        self.message_responder = message_responder

    def put(self, message):
        args = tuple([
            message['type'],
            message['from'],
            message['to'],
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

    def __call__(self, *args, **kwargs):
        if len(args) == 1:
            message = args[0]
            message['from'] = message['from'].bare
            message['to'] = message['to'].bare
        else:
            # {'rtm_client': <slack.rtm.client.RTMClient object at 0x7fb51778f860>, 'web_client': <slack.web.client.WebClient object at 0x7fb515cbca20>, 'data': {'client_msg_id': '91181cfe-5db8-4707-b5dd-90e101c5d68e', 'suppress_notification': False, 'text': 'hi', 'user': 'U04HF1BP9', 'team': 'T04EN147C', 'user_team': 'T04EN147C', 'source_team': 'T04EN147C', 'channel': 'DQA2P16G1', 'event_ts': '1573707936.000400', 'ts': '1573707936.000400'}}
            try:
                slack_message = kwargs['data']
                message = {}
                message['body'] = slack_message['text']
                message['to'] =  slack_message['user']
                message['from'] = slack_message['channel']
                message['status'] = 'whatever'
                message['type'] = 'who cares'
            except KeyError:
                print(kwargs)
                return

        repeats = 1
        if self.is_bomb(message):
            repeats, command, etc = self.parse_bomb(message)
            message['body'] = command + etc
            repeats = min(int(repeats), 50)
        for x in range(0, repeats):
            self.put(message)

