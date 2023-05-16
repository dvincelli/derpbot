from derp.command.finder import CommandFinder
from derp.command.runner import CommandRunner
from derp.command.loader import CommandLoader


def initialize(bot):
    command_loader = CommandLoader()
    command_finder = CommandFinder(command_loader.commands, command_loader.patterns)
    return CommandRunner(command_finder, bot)
