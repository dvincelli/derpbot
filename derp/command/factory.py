from derp.command.handler import CommandHandler
from derp.command.responder import CommandResponder
from derp.command.dispatcher import CommandDispatcher
from derp.command.loader import CommandLoader


def initialize(bot, dispatcher='multiprocessing'):
        command_loader = CommandLoader()
        command_handler = CommandHandler(
                command_loader.commands,
                command_loader.patterns
            )
        command_responder = CommandResponder(bot)
        if dispatcher == 'multiprocessing':
            command_dispatcher = CommandDispatcher(command_handler, command_responder)
            return command_dispatcher
        else:
            raise NotImplementedError
