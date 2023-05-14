import logging
from optparse import OptionParser
import os

import dotenv

from derp.backends.slack import SlackBot

import derp.command.factory


if __name__ == "__main__":
    dotenv.load_dotenv()

    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option(
        "-q",
        "--quiet",
        help="set logging to ERROR",
        action="store_const",
        dest="loglevel",
        const=logging.ERROR,
        default=logging.INFO,
    )
    optp.add_option(
        "-d",
        "--debug",
        help="set logging to DEBUG",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )

    optp.add_option("-s", "--slack-token", dest="slack_token", help="slack bot token")
    optp.add_option("-t", "--slack-app-token", dest="slack_app_token", help="slack app token")
    optp.add_option("-r", "--room", dest="room", help="channel or room to join")
    optp.add_option("-n", "--nick", dest="nick", help="bot nickname", default="enertel.ai")

    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel)

    slack_token = None
    if opts.slack_token:
        slack_token = opts.slack_token
    elif os.getenv("SLACK_TOKEN", None):
        slack_token = os.getenv("SLACK_TOKEN")

    if slack_token is None:
        raise ValueError("You must provide a Slack Bot Token")

    slack_app_token = None
    if opts.slack_app_token:
        slack_app_token = opts.slack_app_token
    elif os.getenv("SLACK_APP_TOKEN", None):
        slack_app_token = os.getenv("SLACK_APP_TOKEN")

    if slack_app_token is None:
        raise ValueError("You must provide a Slack App Token")

    bot = SlackBot(slack_token, slack_app_token, opts.room, opts.nick)

    handler = derp.command.factory.initialize(bot)

    bot.register_message_handler(handler)
    #bot.say('#general', 'hello')

    bot.run()
