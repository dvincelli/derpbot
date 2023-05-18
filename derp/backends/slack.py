from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event
import logging
import os


logger = logging.getLogger(__name__)


class SlackBot:
    def __init__(self, slack_token: str, slack_app_token: str):
        self.socket_client = SocketModeClient(slack_app_token)
        self.web_client = WebClient(token=slack_token)

    @classmethod
    def from_env(cls):
        return cls(os.getenv("SLACK_TOKEN"), os.getenv("SLACK_APP_TOKEN"))

    def register_message_handler(self, handler):
        def process(client: SocketModeClient, req: SocketModeRequest):
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

            return handler(client, req)

        self.handler = handler

        self.socket_client.socket_mode_request_listeners.append(process)

    def handle_request(self, req):
        self.handler(self.socket_client, req)

    def list_commands(self):
        return self.handler.list_commands()

    def run(self):
        self.web_client.api_test()
        self.socket_client.connect()
        Event().wait()

    def say(self, channel, text, thread_ts=None):
        if text is not None:
            self.web_client.chat_postMessage(
                channel=channel, text=text, thread_ts=thread_ts
            )

    def upload(self, title, filename, content) -> str:
        new_file = self.web_client.files_upload_v2(
            title=title,
            filename=filename,
            file=content if hasattr(content, "read") else None,
            content=content if not hasattr(content, "read") else None,
        )
        return new_file.get("file").get("permalink")
