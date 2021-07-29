from math import *

MAXIMUM_LENGTH_OF_NUMBERS = 12

operators = {'*': '*', '/': '/', '+': '+', '-': '-', '^': '**'}
constants = ['pi', 'e']
# Create classes for functions
functions = []
int_functions = {'gcd': 'gcd'}
float_functions = {'abs': 'abs'}


class Functions(object):
    def __init__(self, references, function, num_of_arguments, req_int):
        """
        Initializes an Operator class
        :param references: list of strings, accepted forms of referring to a function
        :param function: string, function references are referring to
        :param num_of_arguments: int, number of arguments taken by a function
        :param req_int: boolean, True if a function requires arguments to be integers, False otherwise
        """
        self.references = references
        self.function = function
        self.num_of_arguments = num_of_arguments
        self.req_int = req_int

    def get_function(self, reference):
        """
        Checks if reference references to this function
        :param reference: string
        :return: function (str), number of arguments (int), does function require arguments to be integers (bool)
        """
        if reference in self.references:
            return self.function, self.num_of_arguments, self.req_int
        return None

    def get_references(self):
        return self.references


def load_functions():
    file = open('functions.txt', 'r')
    for line in file:
        if line[0] != '#':
            line = line.split(':')
            references = line[0].split(' ')
            function = line[1]
            num_of_arguments = int(line[2])
            req_int = bool(line[3])
            functions.append(Functions(references, function, num_of_arguments, req_int))
    print('Calculating.py: ' + str(len(functions)) + ' functions loaded')


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
                first_parenthesis = element.find('(')
                second_parenthesis = element.find(')')
                if first_parenthesis != -1 and second_parenthesis != -1 and second_parenthesis == len(element) - 1:
                    function_not_found = True
                    for index in range(len(functions)):
                        f = functions[index].get_function(element[:first_parenthesis])
                        if f is not None:
                            arguments = element[first_parenthesis + 1: second_parenthesis].split(',')
                            if len(arguments) == f[1]:
                                arguments_are_correct = True
                                for argument in arguments:
                                    if not (((not f[2]) and is_legal_float(argument)) or is_legal_int(argument)):
                                        arguments_are_correct = False
                                        break
                                if arguments_are_correct:
                                    expression += f[0] + element[first_parenthesis:]
                                    function_not_found = False
                            else:
                                raise ArithmeticError
                            break
                    if function_not_found:
                        raise ValueError
                else:
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
