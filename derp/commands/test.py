class EchoCommand:
    command = "echo"

    def parse(self, body):
        return " ".join(body.split(" ")[2:])

    def __call__(self, msg):
        return self.parse(msg["body"])


class PingCommand:
    command = "ping"

    def __call__(self, _):
        return "pong"
