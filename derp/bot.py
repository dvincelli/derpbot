#!/usr/bin/env python
import importlib
import os
import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp

class MUCBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.logger = logging.getLogger('derpbot')
        self.load_commands()

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    def load_commands(self):
        cmdpath = os.path.join(
                os.path.abspath(
                    os.path.dirname(sys.modules['__main__'].__file__)
                ),
                'commands'
            )
        self.commands = {}
        self.patterns = {}
        for cmd in os.listdir(cmdpath):
            if not cmd.endswith('.py'):
                continue
            self.logger.debug('Found %r', cmd)
            modname = os.path.basename(cmd).rstrip('.py')
            self.logger.info(modname)
            module = importlib.import_module('.'.join(['derp.commands', modname]))
            for klassname in [c for c in dir(module) if not c.startswith('__')]:
                self.add_command(module, klassname)
                self.add_pattern(module, klassname)
        self.logger.debug('Loaded commands: %r', self.commands)
        self.logger.debug('Loaded patterns: %r', self.patterns)

    def add_command(self, module, klassname):
        klass = getattr(module, klassname)
        try:
            command = klass.command
            self.commands[klass.command] = klass()
        except AttributeError as e:
            pass

    def add_pattern(self, module, klassname):
        klass = getattr(module, klassname)
        try:
            pattern = klass.pattern
            self.patterns[klass.pattern] = klass()
        except AttributeError as e:
            pass

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        body = msg['body']
        self.logger.debug(body)
        if body.startswith('!'):
            command = body.split(' ', 1)[0][1:]
            self.logger.debug(command)
            self.call_plugin(self.commands.get(command), msg)

        for pattern in self.patterns:
            match = pattern.search(body)
            if match:
                self.logger.debug(body)
                self.call_plugin(self.patterns.get(pattern), msg)

    def call_plugin(self, command, msg):
        if command:
            output = command(msg)
            self.send_message(
                    mto=msg['from'].bare,
                    mbody=output,
                    mtype='groupchat')

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
    #xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=False)
        print("Done")
    else:
        print("Unable to connect.")
