import asyncio
import logging
from derp.command.parser import parse

logger = logging.getLogger(__name__)


class CommandHandler:
    def __init__(self, commands, patterns):
        self.commands = commands
        self.patterns = patterns

    def parse_message(self, body):
        logger.debug('Parsing body %r', body)
        if ' ' in body:
            command = body.split(" ")[1]
            logger.debug('Searching for command %s', command)
            if self.find_command(command):
                logger.debug('Found command %s', command)
                return command

        for pattern in self.patterns:
            logger.debug('Searching for pattern %s', pattern)
            match = pattern.search(body)
            if match:
                logger.debug('Matched pattern %s', pattern)
                return pattern

    def find_command(self, cmdname):
        logger.debug('Looking for %r in %r', cmdname, self.commands)
        return self.commands.get(cmdname, self.patterns.get(cmdname))

    def __call__(self, msg):
        cmdname = self.parse_message(msg['body'])
        command = self.find_command(cmdname)

        if command:
            if getattr(command, 'wants_parse', False):
                args = parse(msg['body'])
            else:
                args = msg

            if not getattr(command, 'is_async', False):
                logger.debug('Running %r with args %r', command, args)
                response = command(args)
            else:
                logger.debug('Awaiting %r with args %r', command, args)
                response = asyncio.run(command(args))

            return msg['from'], response
