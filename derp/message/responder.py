class MessageResponder(object):

    def __init__(self, sleekxmpp):
        self.sleekxmpp = sleekxmpp

    def __call__(self, response):
        try:
            mto, mbody = response
        except TypeError:
            return
        self.sleekxmpp.send_message(mto, mbody, mtype='groupchat')
