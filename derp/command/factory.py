from derp.command.finder import CommandFinder
from derp.command.runner import CommandRunner
from derp.command.loader import CommandLoader


def initialize(bot):
    loader = CommandLoader()
    finder = CommandFinder(loader.commands)
    runner = CommandRunner(finder, bot)
    bot.register_message_handler(runner)
    return bot
