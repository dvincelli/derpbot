from lark import Lark, Transformer


l = Lark('''?start: mention command args

            mention: "<" "@" CNAME ">"

            args: (arg | ((arg)" "+)*) (arg)?

            arg: key "=" value

            symbol: CNAME
            command: CNAME
            key: CNAME
            value: string
                 | int
                 | float
                 | symbol
                 | bool

            string: ESCAPED_STRING
            int: INT
            float: FLOAT


            bool: "true"
                | "false"
                | "True"
                | "False"
                | "0"
                | "1"


            %import common (ESCAPED_STRING, CNAME, INT, FLOAT, WS)

            %ignore WS
         ''')


class CommandTransformer(Transformer):
    def start(self, s):
        return s

    def mention(self, m):
        return ""

    def symbol(self, sym):
        return sym

    def command(self, cmd):
        (cmd,) = cmd
        return cmd.value

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def bool(self, b):
        lb = b.lower()
        if lb == "true":
            return True
        elif lb == "false":
            return False
        elif lb == "0":
            return False
        else:
            # lb == "1"
            return True

    def int(self, i):
        (i,) = i
        return int(i)

    def float(self, f):
        (f,) = f
        return float(f)

    def key(self, k):
        (k,) = k
        return k.value

    def value(self, v):
        (v,) = v
        return v

    arg = tuple

    args = dict


def parse(msg):
    tree = l.parse(msg)
    return CommandTransformer().transform(tree)

#pprint(l.parse('prom query_range="" start="" end=1.23 step="5m"'))
# parse(r'''prom query_range="up { kubernetes_namespace=\"staging\" }" start="5" end=1.23 step="5m"''')
