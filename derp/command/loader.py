import importlib
import os
import sys

import logging

logger = logging.getLogger("derp.command.loader")


class CommandLoader:
    commands = {}
    patterns = {}

    def __init__(self):
        self.load_commands()

    def load_commands(self):
        cmdpath = os.path.join(
            os.path.abspath(os.path.dirname(sys.modules["__main__"].__file__)),
            "commands",
        )
        for cmd in os.listdir(cmdpath):
            if not cmd.endswith(".py"):
                continue
            modname = os.path.basename(cmd)[:-3]  # remove .py
            module = importlib.import_module(".".join(["derp.commands", modname]))
            logger.debug("Imported module: %r", module)
            for klassname in [c for c in dir(module) if not c.startswith("__")]:
                self.add_command(module, klassname)
                self.add_pattern(module, klassname)
        logger.debug("Loaded commands: %r", self.commands)
        logger.debug("Loaded patterns: %r", self.patterns)

    def add_command(self, module, klassname):
        klass = getattr(module, klassname)
        try:
            command = klass.command
            if command:
                self.commands[command] = klass()
        except AttributeError:
            pass

    def add_pattern(self, module, klassname):
        klass = getattr(module, klassname)
        try:
            pattern = klass.pattern
            if pattern:
                self.patterns[pattern] = klass()
        except AttributeError:
            pass
