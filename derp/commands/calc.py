import operator
import re

# While there are tokens to be read:
# Read a token.
# If the token is a number, then add it to the output queue.
# If the token is a function token, then push it onto the stack.
# If the token is a function argument separator (e.g., a comma):
# Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue. If no left parentheses are encountered, either the separator was misplaced or parentheses were mismatched.
# If the token is an operator, o1, then:
# while there is an operator token, o2, at the top of the stack, and
# either o1 is left-associative and its precedence is less than or equal to that of o2,
# or o1 has precedence less than that of o2,
# pop o2 off the stack, onto the output queue;
# push o1 onto the stack.
# If the token is a left parenthesis, then push it onto the stack.
# If the token is a right parenthesis:
# Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue.
# Pop the left parenthesis from the stack, but not onto the output queue.
# If the token at the top of the stack is a function token, pop it onto the output queue.
# If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
# When there are no more tokens to read:
# While there are still operator tokens in the stack:
# If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
# Pop the operator onto the output queue.

class ParseError(Exception):
    pass

class CalculatorCommand(object):

    command = 'calc'

    def to_postfix(self, infix):
        stack = []
        output = []
        input = iter(infix)
        token = self.next_token(input)
        prec = {
            '*': 3,
            '/': 3,
            '%': 3,
            '+': 2,
            '-': 2,
        }
        for token in self.next_token(input):
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

    def next_token(self, input):
        # lol u need a real lexer
        token = ''
        for x in input:
            if x == ' ':
                if token:
                    yield int(token)
                    token = ''

            if x.isdigit():
                token += x

            if x in '*/+-%()':
                if token:
                    yield int(token)
                    token = ''
                yield x

        if token:
            yield int(token)

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
        postfix = self.to_postfix(msg['body'].lstrip('!' + self.command))
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
