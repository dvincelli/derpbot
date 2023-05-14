import itertools
import operator
import re


class ParseError(Exception):
    pass


OP_ADD = "+"
OP_SUB = "-"
OP_MUL = "*"
OP_DIV = "/"
OP_MOD = "%"
OP_EXP = "^"
OPERATORS = OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD, OP_EXP

SYM_LPAREN = "("
SYM_RPAREN = ")"


class CalculatorCommand:
    command = "calc"

    def is_operator(self, token):
        return token in OPERATORS

    def op_left_assoc(self, token):
        if token == OP_EXP:
            return False
        return True

    def op_prec(self, token):
        if token == OP_EXP:
            return 4
        if token in (OP_MUL, OP_DIV, OP_MOD):
            return 3
        if token in (OP_ADD, OP_SUB):
            return 2
        if token == SYM_LPAREN:
            return 1
        if token == SYM_RPAREN:
            return 0

    def to_postfix(self, infix):
        stack = []
        output = []
        input = iter(infix)

        for token in self.tokenize(input):
            if isinstance(token, (float, int)):
                output.append(token)

            elif self.is_operator(token):
                if len(stack) == 0:
                    stack.append(token)
                elif stack[-1] == SYM_LPAREN:
                    stack.append(token)
                else:
                    op1 = token
                    if self.op_left_assoc(op1):
                        while len(stack) > 0 and self.op_prec(op1) <= self.op_prec(
                            stack[-1]
                        ):
                            op2 = stack.pop()
                            output.append(op2)
                    else:
                        while len(stack) > 0 and self.op_prec(op1) < self.op_prec(
                            stack[-1]
                        ):
                            op2 = stack.pop()
                            output.append(op2)
                    stack.append(op1)

            elif token == SYM_LPAREN:
                stack.append(token)

            elif token == SYM_RPAREN:
                while len(stack) > 0 and stack[-1] != SYM_LPAREN:
                    op = stack.pop()
                    output.append(op)
                if len(stack) > 0 and stack[-1] == SYM_LPAREN:
                    stack.pop()

        while len(stack) > 0:
            op = stack.pop()
            if op == SYM_LPAREN:
                raise ParseError
            output.append(op)

        if SYM_RPAREN in output:
            raise ParseError

        return output

    def tokenize(self, input):
        token = ""
        input_iter = iter(input)
        done = [False]

        def next_char(input_iter):
            try:
                return next(input_iter)
            except StopIteration:
                done[0] = True
                return ""

        while not done[0]:
            x = next_char(input_iter)
            if x.isdigit():
                while x.isdigit():
                    token += x
                    x = next_char(input_iter)
                if x == ".":
                    token += x
                    x = next_char(input_iter)
                    while x.isdigit():
                        token += x
                        x = next_char(input_iter)
                    yield float(token)
                    token = ""
                else:
                    yield int(token)
                    token = ""

            if x == "-":
                x = next_char(input_iter)
                if x.isdigit():
                    token += "-"
                    while x.isdigit():
                        token += x
                        x = next_char(input_iter)
                    if x == ".":
                        token += x
                        x = next_char(input_iter)
                        while x.isdigit():
                            token += x
                            x = next(input_iter)
                        yield float(token)
                        token = ""
                    else:
                        yield int(token)
                        token = ""
                else:
                    yield OP_SUB
                    # push back
                    input_iter = itertools.chain([x], input_iter)
                    continue

            elif x in OPERATORS or x in (SYM_LPAREN, SYM_RPAREN):
                yield x
            elif x == "":  # kludge for EOL
                break
            elif x != " ":  # eat spaces, anything else is unrecognized
                raise ParseError

    def eval(self, infix):
        stack = []
        ops = {
            OP_EXP: operator.pow,
            OP_MUL: operator.mul,
            OP_DIV: operator.truediv,
            OP_MOD: operator.mod,
            OP_ADD: operator.add,
            OP_SUB: operator.sub,
        }
        for token in infix:
            if isinstance(token, (float, int)):
                stack.append(token)
            elif token in OPERATORS:
                op = ops.get(token)
                term = stack.pop()
                factor = stack.pop()
                result = op(factor, term)
                stack.append(result)
        if len(stack) == 1:
            return stack.pop()
        else:
            raise ParseError(" ".join(map(str, stack)))

    def __call__(self, msg):
        try:
            expr = msg["body"][len(self.command) + 1 :].strip()
            postfix = self.to_postfix(expr)
        except ParseError:
            return "parse error: " + expr
        return expr + " = " + str(self.eval(postfix))


class RPNCalculatorCommand(CalculatorCommand):
    command = "rpn"

    re_int = re.compile("^-?\d+$")
    re_float = re.compile("^-?\d+\.\d+$")

    def __call__(self, msg):
        input = msg["body"][len(self.command) + 1 :].strip().split(" ")
        postfix = []
        for item in input:
            if self.re_int.match(item):
                postfix.append(int(item))
            elif self.re_float.match(item):
                postfix.append(float(item))
            elif item:
                postfix.append(item)
        return " ".join(input) + " = " + str(self.eval(postfix))
