import logging

logger = logging.getLogger(__name__)


class CommandFinder:
    def __init__(self, commands):
        self.commands = commands

    def parse_message(self, text):
        logger.debug("Parsing message text %r", text)
        try:
            command = text.split(" ")[1]
        except IndexError:
            logger.debug("Message malformed. Could not locate command.")
            return

        logger.debug("Searching for command %s", command)
        if self.find_command(command):
            logger.debug("Found command %s", command)
            return command

    def find_command(self, cmdname):
        logger.debug("Looking for %r in %r", cmdname, self.commands)
        return self.commands.get(cmdname)

    def __call__(self, msg):
        cmdname = self.parse_message(msg["body"])
        return self.find_command(cmdname)
