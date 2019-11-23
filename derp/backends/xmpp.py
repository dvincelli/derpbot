import sleekxmpp


class XMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)

    def register_message_handler(self, handler):
        self.add_event_handler("groupchat_message", handler)

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin["xep_0045"].joinMUC(
            self.room,
            self.nick,
            # If a room password is needed, use:
            # password=the_room_password,
            wait=True,
        )

    def run(self):
        self.connect()

        self.register_plugin("xep_0060")  # PubSub
        self.register_plugin("xep_0045")  # Multi-User Chat
        sekf.register_plugin(
            "xep_0199", pconfig={"keepalive": True, "interval": 15, "timeout": 5}
        )  # XMPP Ping

        if self.connect():
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            self.whitespace_keepalive_interval = 30
            self.process(block=False)
        else:
            raise RuntimeError("Unable to connect.")
