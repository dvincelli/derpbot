from lark import Lark, Transformer


keypair_lang = Lark(
    """?start: mention? command args

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


            %import common (ESCAPED_STRING, CNAME, INT, FLOAT, WS)

            %ignore WS
         """
)


class KeypairCommandTransformer(Transformer):
    def start(self, s):
        return s

    def mention(self, m):
        (m,) = m
        return f"<@{m.value}>"

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


def parse(text: str):
    tree = keypair_lang.parse(text)
    return KeypairCommandTransformer().transform(tree)
