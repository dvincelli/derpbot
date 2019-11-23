import slack  # python-slackclient
from pprint import pprint


class SlackBot:
    def __init__(self, slack_token: str, channel: str, nick: str):
        self.channel = channel
        self.nick = nick
        self.rtm_client = slack.RTMClient(token=slack_token)
        self.web_client = slack.WebClient(token=slack_token)

    def register_message_handler(self, handler):
        slack.RTMClient.run_on(event="message")(handler)

    def run(self):
        self.rtm_client.start()

    def send_message(self, to, body, **kwargs):
        self.web_client.chat_postMessage(
            channel=to, text=body or "Nothing",
        )
