class CommandHandler(object):
    def __init__(self, commands, patterns):
        self.commands = commands
        self.patterns = patterns

    def parse_message(self, body):
        if body.startswith("!"):
            command = body.split(" ", 1)[0]
            return command

        for pattern in self.patterns:
            match = pattern.search(body)
            if match:
                return pattern

    def find_command(self, cmdname):
        return self.commands.get(cmdname, self.patterns.get(cmdname))

    def __call__(self, mtype, mfrom, mto, body, status):
        cmdname = self.parse_message(body)
        command = self.find_command(cmdname)

        if command:
            msg = {
                "type": mtype,
                "from": mfrom,
                "to": mto,
                "body": body,
                "status": status,
            }
            output = command(msg)
            return mfrom, output
