from slack_sdk  import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event
import os


class SlackBot:
    def __init__(self, slack_token: str, slack_app_token: str):
        self.socket_client = SocketModeClient(slack_app_token)
        self.web_client = WebClient(token=slack_token)

    @classmethod
    def from_env(cls):
        return cls(os.getenv('SLACK_TOKEN'), os.getenv('SLACK_APP_TOKEN'))

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

    def upload(self, title, filename, content) -> str:
        new_file = self.web_client.files_upload_v2(
                title=title,
                filename=filename,
                file=content if hasattr(content, 'read') else None,
                content=content if not hasattr(content, 'read') else None,
            )
        return new_file.get('file').get('permalink')
