from derp.commands.images import ImageCommand


def test_image_command():
    msg = {"body": "!img test"}

    ImageCommand()(msg)
