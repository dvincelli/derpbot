from typing import TypedDict, Union, NotRequired
from io import BytesIO
from derp.backends.slack import SlackBot


class SayArgs(TypedDict):
    channel: NotRequired[str]
    text: str
    thread_ts: NotRequired[str]


class UploadArgs(TypedDict):
    title: str
    filename: str
    content: Union[BytesIO, str, bytes]


class ShareFileArgs(TypedDict):
    channel: NotRequired[str]
    text: str
    thread_ts: NotRequired[str]

    title: str
    filename: str
    content: Union[BytesIO, str, bytes]


class BaseResponse:
    def __init__(self, args):
        self.args = args

    def update(self, args):
        self.args.update(args)

    def __call__(self, bot: SlackBot):
        raise NotImplementedError()


class SayResponse(BaseResponse):
    def __init__(self, args: SayArgs):
        self.args = args

    def __call__(self, slackbot: SlackBot):
        return slackbot.say(**self.args)


class UploadResponse(BaseResponse):
    def __init__(self, args: UploadArgs):
        self.args = args

    def __call__(self, bot: SlackBot) -> str:
        return bot.upload(**self.args)


class ShareFileResponse(BaseResponse):
    def __init__(self, args: ShareFileArgs):
        self.args = args

    def __call__(self, bot: SlackBot):
        file_url = bot.upload(
            title=self.args['title'],
            filename=self.args['filename'],
            content=self.args['content']
        )
        text = self.args['text'].format(file_url=file_url)

        if self.args.get('channel') is None:
            raise ValueError('No channel found in args')

        return bot.say(
            channel=self.args.get('channel'),
            thread_ts=self.args.get('thread_ts'),
            text=text
        )

