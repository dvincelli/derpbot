from derp.command.finder import CommandFinder


class MockCommand1:
    pass


class MockCommand2:
    pass


def test_finds_commands():
    finder = CommandFinder({"cmd1": MockCommand1(), "cmd2": MockCommand2()})

    assert isinstance(finder.find_command("cmd1"), MockCommand1)
    assert isinstance(finder.find_command("cmd2"), MockCommand2)
    assert finder.find_command("fake") is None
