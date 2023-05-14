import asyncio


class CommandHandler:
    def __init__(self, commands, patterns):
        self.commands = commands
        self.patterns = patterns

    def parse_message(self, body):
        if '!' in body:
            command = body.split(" ", 1)[1]
            return command

        for pattern in self.patterns:
            match = pattern.search(body)
            if match:
                return pattern

    def find_command(self, cmdname):
        return self.commands.get(cmdname, self.patterns.get(cmdname))

    def __call__(self, mfrom, mto, body):
        cmdname = self.parse_message(body)
        command = self.find_command(cmdname)

        if command:
            msg = {
                "from": mfrom,
                "to": mto,
                "body": body,
            }
            if not getattr(command, 'is_async', False):
                output = command(msg)
            else:
                output = asyncio.run(command(msg))

            return mfrom, output
