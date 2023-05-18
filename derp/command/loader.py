import importlib
import importlib.resources
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
        for cmd in importlib.resources.files("derp.commands").iterdir():
            with importlib.resources.as_file(cmd) as file:
                if not file.suffix != "py":
                    continue
                modname = file.stem
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
