from derp.command.response import SayResponse, SayArgs


class ListCommandResponse(SayResponse):
    def __call__(self, bot):
        self.args['text'] = '\n'.join(bot.list_commands())
        return super().__call__(bot)


class ListCommand:
    command = "list"

    def __call__(self, msg):
        return ListCommandResponse(args=SayArgs(text=""))
