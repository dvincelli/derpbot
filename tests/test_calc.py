from derp.commands.calc import CalculatorCommand, RPNCalculatorCommand

def test_complex_formula():
    c = CalculatorCommand()
    answer = c({'body': '!calc 2 * (2 * (4 + 6 + 1) + 1)'})
    assert answer == '2 * (2 * (4 + 6 + 1) + 1) = 46', answer + ' should be 46'

def test_complex_rpn_formula():
    c = RPNCalculatorCommand()
    answer = c({'body': '!rpn 2 2 8 6 + 1 + * 1 + *'})
    assert answer == '2 2 8 6 + 1 + * 1 + * = 62', answer + ' should be 62'

def test_wikipedia_rpn_formula():
    c = RPNCalculatorCommand()
    answer = c({'body': '!rpn 5 1 2 + 4 * + 3 -'})
    assert answer == '5 1 2 + 4 * + 3 - = 14'

def test_infix_to_postfix_simple_formula():
    c = CalculatorCommand()
    answer = c({'body': '!calc (2 * (2 * 3 + 1))'})
    assert answer == '(2 * (2 * 3 + 1)) = 14'


