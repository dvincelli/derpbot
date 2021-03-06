import logging


logger = logging.getLogger(__name__)


class CommandResponder(object):
    def __init__(self, bot):
        self.bot = bot

    def __call__(self, response):
        logger.debug('response is %s', response)
        try:
            mto, mbody = response
        except TypeError:
            return
        self.bot.send_message(mto, mbody, mtype="groupchat")
