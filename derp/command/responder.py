import logging


logger = logging.getLogger(__name__)


class CommandResponder:
    def __init__(self, bot):
        self.bot = bot

    def __call__(self, response):
        logger.debug('response is %s', response)
        try:
            to, text = response
        except TypeError:
            return
        self.bot.say(to, text)
