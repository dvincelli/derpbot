import logging


logger = logging.getLogger(__name__)


class CommandResponder:
    def __init__(self, bot):
        self.bot = bot

    def __call__(self, response):
        logger.debug('response is %r', response)
        # This is weird, feels useless. Should refactor.

        try:
            channel, text = response
        except TypeError as e:
            logger.error(e)
            return

        if callable(text):
            if text.args.get('channel') is None:
                text.args['channel'] = channel
            return text(self.bot)

        self.bot.say(channel=channel, text=text)
