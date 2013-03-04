import itertools
import operator
import re

class ParseError(Exception):
    pass

class CalculatorCommand(object):

    command = 'calc'

    def to_postfix(self, infix):
        stack = []
        output = []
        input = iter(infix)
        prec = {
            '*': 3,
            '/': 3,
            '%': 3,
            '+': 2,
            '-': 2,
        }
        for token in self.tokenize(input):
            if isinstance(token, (float, int)):
                output.append(token)

            elif token == '(':
                stack.append(token)

            elif token == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    op = stack.pop()
                    output.append(op)
                if len(stack) > 0 and stack[-1] == '(':
                    stack.pop()

            elif token in '+-*/%':
                if len(stack) == 0 or stack[-1] == '(':
                    stack.append(token)
                else:
                    op1 = token
                    while len(stack) > 0 and stack[-1] != '(' and stack[-1] in '+-*/%' and prec[op1] <= prec[stack[-1]]:
                            op2 = stack.pop()
                            output.append(op2)
                    stack.append(op1)

        if len(stack) > 0 and stack[-1] == '(':
            raise ParseError

        while len(stack) > 0:
            op = stack.pop()
            output.append(op)

        if ')' in output:
            raise ParseError

        return output

    def tokenize(self, input):
        token = ''
        input_iter = iter(input)
        done = [False]

        def next_char(input_iter):
            try:
                return next(input_iter)
            except StopIteration:
                done[0] = True
                return ''

        while not done[0]:
            x = next_char(input_iter)
            if x.isdigit():
                while x.isdigit():
                    token += x
                    x = next_char(input_iter)
                if x == '.':
                    token += x
                    x = next_char(input_iter)
                    while x.isdigit():
                        token += x
                        x = next_char(input_iter)
                    yield float(token)
                    token = ''
                else:
                    yield int(token)
                    token = ''
                    input_iter = itertools.chain([x], input_iter)

            if x == '-':
                x = next_char(input_iter)
                if x.isdigit():
                    token += '-'
                    while x.isdigit():
                        token += x
                        x = next_char(input_iter)
                    if x == '.':
                        token += x
                        x = next_char(input_iter)
                        while x.isdigit():
                            token += x
                            x = next(input_iter)
                        yield float(token)
                        token = ''
                    else:
                        yield int(token)
                        token = ''
                else:
                    input_iter = itertools.chain([x], input_iter)

            if x in '*/+-%()':
                if x != '':  # EOF
                    yield x
            elif x != ' ':   # eat spaces, anything else is unrecognized
                raise ParseError

    def eval(self, infix):
        print('Evaluating: %s' % infix)
        stack = []
        ops = {
                '*': operator.mul,
                '/': operator.div,
                '%': operator.mod,
                '+': operator.add,
                '-': operator.sub
            }
        for token in infix:
            if isinstance(token, (float, int)):
                stack.append(token)
            elif token in '*/%+-':
                op = ops.get(token)
                term = stack.pop()
                factor = stack.pop()
                result = op(factor, term)
                stack.append(result)
        return stack.pop()

    def __call__(self, msg):
        try:
            postfix = self.to_postfix(msg['body'].lstrip('!' + self.command))
        except ParseError as e:
            return str(e)
        return str(self.eval(postfix))


class RPNCalculatorCommand(CalculatorCommand):
    command = 'rpn'

    re_int = re.compile('^-?\d+$')
    re_float = re.compile('^-?\d+\.|e\d+$')

    def __call__(self, msg):
        input = msg['body'].lstrip('!' + self.command).split(' ')
        postfix = []
        for item in input:
            if self.re_int.match(item):
                postfix.append(int(item))
            elif self.re_float.match(item):
                postfix.append(float(item))
            elif item:
                postfix.append(item)
        return str(self.eval(postfix))
