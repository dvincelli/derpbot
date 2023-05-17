from derp.command.parser import parse


def test_keypair_parse():
    transformed = parse(
        '<@mention> cmd k=pair k1=1 k2="foo bar" k3=3.14 k4=true k5=false'
    )
    assert transformed == [
        "<@mention>",
        "cmd",
        {"k": "pair", "k1": 1, "k2": "foo bar", "k3": 3.14, "k4": True, "k5": False},
    ]


def test_keypair_parse__nulls():
    transformed = parse("<@mention> cmd k=None k1=nil k2=none k3=null")

    assert transformed == [
        "<@mention>",
        "cmd",
        {"k": None, "k1": None, "k2": None, "k3": None},
    ]
