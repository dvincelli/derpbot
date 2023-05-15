import random
import os


class FortuneCommand:
    command = "fortune"

    def __call__(self, msg):
        path = os.path.join(os.path.dirname(__file__), "..", "fortunes", self.command)
        filesize = os.path.getsize(path)
        fortune_file = open(path, "rb")

        startpos = random.randint(0, filesize)
        fortune_file.seek(startpos)
        x = fortune_file.read(1)
        buf = bytes()

        while x != b"%":
            filepos = fortune_file.tell()
            if filepos < 1:
                break

            fortune_file.seek(filepos - 1, os.SEEK_SET)
            x = fortune_file.read(1)
            fortune_file.seek(fortune_file.tell() - 1, os.SEEK_SET)

        fortune_file.seek(fortune_file.tell() + 1, os.SEEK_SET)
        x = fortune_file.read(1)

        while x != b"%":
            if x == b"":
                break

            buf += x
            x = fortune_file.read(1)

        try:
            return buf.decode()
        finally:
            fortune_file.close()


class StarTrekCommand(FortuneCommand):
    command = "startrek"


class HomerSimpsonCommand(FortuneCommand):
    command = "homer"


class RalphWiggumsCommand(FortuneCommand):
    command = "ralph"


class BartDetentionCommand(FortuneCommand):
    command = "bart"


class CalinAndHobbesCommand(FortuneCommand):
    command = "calvin"


class ComicBookGuyCommand(FortuneCommand):
    command = "comic"


class ProgStyleCommand(FortuneCommand):
    command = "prog-style"


class SeinfeldCommand(FortuneCommand):
    command = "seinfeld"


class BmcCommand(FortuneCommand):
    command = "bmc"
