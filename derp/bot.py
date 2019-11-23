#!/usr/bin/env python
import logging
import getpass
from optparse import OptionParser

from derp.backends.xmpp import XMPPBot
from derp.backends.slack import SlackBot
import derp.command.factory


if __name__ == "__main__":
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
    optp.add_option(
        "-v",
        "--verbose",
        help="set logging to COMM",
        action="store_const",
        dest="loglevel",
        const=5,
        default=logging.INFO,
    )

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid", help="JID to use (if using XMPP)")
    optp.add_option("-p", "--password", dest="password", help="password to use")
    optp.add_option("-r", "--room", dest="room", help="channel or room to join")
    optp.add_option("-n", "--nick", dest="nick", help="bot nickname")
    optp.add_option("-s", "--slack-token", dest="slack_token", help="slack API token")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel, format="%(levelname)-8s %(message)s")

    if opts.jid:
        bot = XMPPBot(
            opts.jid, opts.password, opts.room, opts.nick, message_handler=handler
        )
    elif opts.slack_token:
        bot = SlackBot(opts.slack_token, opts.room, opts.nick)

    handler = derp.command.factory.initialize(bot)
    bot.register_message_handler(handler)

    bot.run()
