import random
import os

class FortuneCommand(object):
    command = 'fortune'

    def __call__(self, msg):
        path = os.path.join(os.path.dirname(__file__), '..',
                'fortunes', self.command)
        filesize = os.path.getsize(path)
        fortune_file = open(path)

        fortune = []

        fortune_file.seek(random.randint(0, filesize), 0)
        x = fortune_file.read(1)

        while x != '%':
            fortune_file.seek(-1, 1)
            x = fortune_file.read(1)
            fortune_file.seek(-1, 1)

        fortune_file.seek(1, 1)
        x = fortune_file.read(1)

        while x != '%':
            fortune.append(x)
            x = fortune_file.read(1)

        try:
            return ''.join(fortune)
        finally:
            fortune_file.close()

class StarTrekCommand(FortuneCommand):
    command = 'startrek'

class HomerSimpsonCommand(FortuneCommand):
    command = 'homer'

class RalphWiggumsCommand(FortuneCommand):
    command = 'ralph'

class BartDetentionCommand(FortuneCommand):
    command = 'bart'

class CalinAndHobbesCommand(FortuneCommand):
    command = 'calvin'

class ComicBookGuyCommand(FortuneCommand):
    command = 'comic'

class ProgStyleCommand(FortuneCommand):
    command = 'prog-style'

class SeinfeldCommand(FortuneCommand):
    command = 'seinfeld'

class BmcCommand(FortuneCommand):
    command = 'bmc'
