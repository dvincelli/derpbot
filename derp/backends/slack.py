from slack_sdk  import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event


class SlackBot:
    def __init__(self, slack_token: str, slack_app_token: str, channel: str, nick: str):
        self.channel = channel
        self.nick = nick
        self.socket_client = SocketModeClient(slack_app_token)
        self.web_client = WebClient(token=slack_token)

    def register_message_handler(self, handler):
        def process(client: SocketModeClient, req: SocketModeRequest):
            print(client, req)
            return handler(client, req)
        self.socket_client.socket_mode_request_listeners.append(process)

    def run(self):
        self.web_client.api_test()
        self.socket_client.connect()
        Event().wait()

    def say(self, to, body):
        self.web_client.chat_postMessage(
            channel=to, text=body or "Nothing",
        )
