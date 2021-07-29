from math import *

MAXIMUM_LENGTH_OF_NUMBERS = 12

operators = {'*': '*', '/': '/', '+': '+', '-': '-', '^': '**'}
constants = ['pi', 'e']
# Create classes for functions
int_functions = {'gcd': 'gcd'}
float_functions = {'abs': 'abs'}


def is_legal_float(string):
    """
    :string: a string
    :return: True if string is a float, False otherwise
    """
    try:
        float(string)
        if len(string) <= MAXIMUM_LENGTH_OF_NUMBERS:
            return True
        else:
            raise OverflowError
    except ValueError:
        return False


def is_legal_int(string):
    """
        :string: a string
        :return: True if string is an int, False otherwise
        """
    try:
        int(string)
        if len(string) <= MAXIMUM_LENGTH_OF_NUMBERS:
            return True
        else:
            raise OverflowError
    except ValueError:
        return False


def get_input(user_input):
    """
    Changes input into a legal mathematical expression
    :param user_input: string
    :return: safe string that can be eval'd
    """
    expression = ''
    user_input = user_input.lower()
    # user_input = user_input.replace(',', '.')
    user_input = user_input.split(' ')
    while True:
        try:
            user_input.remove('')
        except ValueError:
            break
    prev_is_operator = True
    if user_input[0] == '':
        raise ValueError
    for element in user_input:
        if prev_is_operator:
            if is_legal_float(element):
                expression += ' ' + element
                prev_is_operator = False
            elif element[-1] == '!' and is_legal_int(element[0:-1]):
                if int(element[0:-1]) < 100:
                    expression += 'factorial(' + element[0:-1] + ') '
                    prev_is_operator = False
                else:
                    raise OverflowError
            else:
                function_not_found = True
                for f in int_functions.keys():
                    if element.find(f + '(') == 0 and element[-1] == ')':
                        length_of_f = len(f)
                        elements = element[length_of_f + 1:-1].split(',')
                        if is_legal_int(elements[0]) and is_legal_int(elements[1]):
                            expression += int_functions[f] + element[length_of_f:]
                            function_not_found = False
                            break
                if function_not_found:
                    for f in float_functions.keys():
                        if element.find(f + '(') == 0 and element[-1] == ')':
                            length_of_f = len(f)
                            if is_legal_int(element[length_of_f + 1:-1]):
                                expression += float_functions[f] + element[length_of_f:]
                                function_not_found = False
                                break
                    if function_not_found:
                        raise ValueError
        elif element in operators.keys():
            expression += ' ' + operators[element]
            prev_is_operator = True
        else:
            raise ValueError
    return expression


def calc(user_input):
    user_input = get_input(user_input)
    return eval(user_input)
