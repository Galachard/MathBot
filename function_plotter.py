import matplotlib.pyplot as plt

start_x_default = -10.0
end_x_default = 10.0
points_default = 100.0

operators = ['*', '/', '+', '-']
functions = ['sin', 'cos', 'tan', 'tg', 'ctan', 'ctg']
constants = ['pi', 'e']

pi = 3.14159265359
e = 2.71828182846


def is_float(string):
    """
    :string: a string
    :return: True if string is a float, False otherwise
    """
    try:
        float(string)
        if len(string) < 25:
            return True
        else:
            raise OverflowError
    except ValueError:
        return False


def get_equation_discord(user_input):
    """
        Asks for an equation in input.
        :return: A correct and legal function, with argument marked as 'x'
        """
    equation = ''
    user_input = user_input.lower()
    user_input = user_input.replace(',', '.')
    user_input = user_input.split(' ')
    while True:
        try:
            user_input.remove('')
        except ValueError:
            break
    prev_is_operator = True
    if user_input[0] != '':
        for element in user_input:
            if 'x' in element:
                length = len(element)
                # 'x' case
                if length == 1 and prev_is_operator:
                    equation += 'x '
                elif length == 1 and not prev_is_operator:
                    equation += '* x '
                # 'x' ^ int case
                elif element.index('x') == 0 and len(element) >= 3 and element[1] == '^' \
                        and is_float(element[2: len(element)]):
                    if prev_is_operator:
                        equation += '(x) ** ' + element[2: len(element)] + ' '
                    else:
                        equation += '* (x) ** ' + element[2: len(element)] + ' '
                # int + 'x' ^ int case
                elif is_float(element[0: element.index('x')]) and prev_is_operator:
                    if element[-1] == 'x':
                        equation += element[0:-1] + ' * ' + 'x '
                    elif element[element.index('x') + 1] == '^' \
                            and is_float(element[element.index('x') + 2: len(element)]):
                        equation += element[0: element.index('x')] + ' * (x) ** ' + \
                                    element[element.index('x') + 2: len(element)] + ' '
                    else:
                        raise ValueError
                else:
                    raise ValueError
                prev_is_operator = False
            # int case
            elif prev_is_operator:
                if is_float(element):
                    equation += element + ' '
                elif element in constants:
                    equation += element + ' '
                else:
                    raise ValueError
                prev_is_operator = False
            # operator case
            elif element in operators and not prev_is_operator:
                equation += element + ' '
                prev_is_operator = True
            else:
                raise ValueError
    else:
        raise ValueError
    return equation


def calculate(equation, x):
    """
    Calculates value of function given by equation for argument x
    :param equation: equation of a function - a string with or without arguments 'x'
    :param x: argument, float
    :return: f(x)
    """
    eq_for_x = equation.replace('x', str(x))
    return eval(eq_for_x)


def plot_graph(f_x, start_x=start_x_default, end_x=end_x_default, start_y=None, end_y=None, points=points_default):
    """
    Sends the graph of a function
    :return: Nothing
    """
    xs = []
    ys = []

    current_x = start_x
    tick = (end_x - start_x) / points

    while current_x <= end_x:
        xs.append(current_x)
        ys.append(calculate(f_x, current_x))
        current_x += tick

    plt.plot(xs, ys)
    plt.savefig("./images/graph.png")
    plt.clf()


def plot(user_input):
    f_x = get_equation_discord(user_input)
    plot_graph(f_x)

# TO DO: Make trigonometric functions work in equations
# ALSO: make constants and functions a dictionary of type 'INPUT':'ACTUAL MEANING', for example 'tg':'tan'
