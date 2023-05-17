from derp.command.parser import parse


def test_parse():
    transformed = parse(
        '<@mention> cmd k=pair k1=1 k2="foo bar" k3=3.14 k4=true k5=false'
    )
    assert transformed == [
        "<@mention>",
        "cmd",
        {"k": "pair", "k1": 1, "k2": "foo bar", "k3": 3.14, "k4": True, "k5": False},
    ]
