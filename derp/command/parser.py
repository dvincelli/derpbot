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
                 | bool
                 | symbol

            string: ESCAPED_STRING
            int: INT
            float: FLOAT

            bool: "true"    -> true
                | "True"    -> true
                | "false"   -> false
                | "False"   -> false

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
        (sym,) = sym
        return sym.value

    def command(self, cmd):
        (cmd,) = cmd
        return cmd.value

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def true(self, _):
        return True

    def false(self, _):
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
