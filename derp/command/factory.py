from derp.command.handler import CommandHandler
from derp.command.responder import CommandResponder
from derp.command.dispatcher import CommandDispatcher
from derp.command.loader import CommandLoader


def initialize(bot):
    command_loader = CommandLoader()
    command_handler = CommandHandler(command_loader.commands, command_loader.patterns)
    command_responder = CommandResponder(bot)
    return CommandDispatcher(command_handler, command_responder)
