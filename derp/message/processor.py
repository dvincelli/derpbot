from derp.command_loader import CommandLoader
import random

class MessageProcessor(object):

    @property
    def commands(self):
        try:
            return self._commands
        except AttributeError:
            self._commands = CommandLoader().commands
            return self._commands

    @property
    def patterns(self):
        try:
            return self._patterns
        except AttributeError:
            self._patterns = CommandLoader().patterns
            return self._patterns

    def parse_message(self, body):
        if body.startswith('!'):
            command = body.split(' ', 1)[0]
            return command.strip()

        for pattern in self.patterns:
            match = pattern.search(body)
            if match:
                return pattern

    def find_command(self, cmdname):
        try:
            return self.commands[cmdname]
        except KeyError:
            try:
                return self.patterns[cmdname]
            except KeyError:
                return None

    def __call__(self, mtype, mfrom, mto, body, status):
        try:
            cmdname = self.parse_message(body)
            command = self.find_command(cmdname)

            if command:
                msg = {
                        'type': mtype,
                        'from': mfrom,
                        'to': mto,
                        'body': body,
                        'status': status
                    }
                output = command(msg)
                return mfrom, output
        except Exception as e:
            return mto, str(e)
