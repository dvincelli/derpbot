import logging
from derp.command.parser import parse

logger = logging.getLogger(__name__)


class CommandRunner:
    def __init__(self, command_finder, bot):
        self.find_command = command_finder
        self.bot = bot

    def _respond(self, response, thread_ts):
        logger.debug("response is %r", response)

        # legacy commands return a tuple
        try:
            channel, text = response
        except TypeError as e:
            logger.error(e)
            return

        # New way: callable responder
        if callable(text):
            if text.args.get("channel") is None:
                text.args["channel"] = channel
            if text.args.get("thread_ts") is None:
                text.args["thread_ts"] = thread_ts
            return text(self.bot)

        self.bot.say(channel=channel, text=text, thread_ts=thread_ts)

    def _run(self, msg, command):
        if getattr(command, "wants_parse", False):
            args = parse(msg["body"])
        else:
            args = msg

        logger.debug("Running %r with args %r", command, args)
        response = command(args)

        return msg["from"], response

    def __call__(self, client, req):
        try:
            logger.info("req %r", req)

            slack_message = req.to_dict()["payload"]["event"]
            logger.debug("slack_message %r", slack_message)

            if slack_message.get("subtype") == "bot_message":
                logger.debug("Ignored, subtype is botmessage ...")
                # ignore ourself
                return

            # Soon we can refactor this away
            message = {}
            message["body"] = slack_message["text"]
            message["to"] = slack_message["user"]
            message["from"] = slack_message["channel"]
            thread_ts = slack_message.get("ts")

            command = self.find_command(message)
            response = self._run(message, command)

            self._respond(response, thread_ts)

        except KeyError as e:
            logger.exception("%s while handling message", e)
            return
