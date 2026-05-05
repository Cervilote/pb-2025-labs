class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top_node = None
        self.size = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top_node
        self.top_node = new_node
        self.size += 1

    def pop(self):
        if self.is_empty():
            return None
        value = self.top_node.value
        self.top_node = self.top_node.next
        self.size -= 1
        return value

    def top(self):
        if self.is_empty():
            return None
        return self.top_node.value

    def is_empty(self):
        return self.top_node is None


def infix_to_postfix(expression):
    if not expression.strip():
        return None, "Error: empty expression"

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
    right_associative = {'**'}
    tokens = expression.split()
    output = []
    operator_stack = Stack()

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Определяем, является ли текущий '-' унарным минусом
        is_unary_minus = (token == '-' and
                          (i == 0 or
                           tokens[i - 1] in '(+-*/**'))

        if is_unary_minus:

            if i + 1 < len(tokens) and tokens[i + 1].replace('.', '', 1).isdigit():
                combined = '-' + tokens[i + 1]
                output.append(combined)
                i += 2
                continue
            else:
                return None, "Error: invalid token '-'"


        if token.replace('.', '', 1).replace('-', '', 1).isdigit():
            output.append(token)

        elif token == '(':
            operator_stack.push(token)

        elif token == ')':
            found_open = False
            while not operator_stack.is_empty() and operator_stack.top() != '(':
                output.append(operator_stack.pop())
                found_open = True
            if operator_stack.is_empty():
                return None, "Error: mismatched parentheses"
            operator_stack.pop()  # убираем '('

        elif token in precedence:
            while (not operator_stack.is_empty() and
                   operator_stack.top() != '(' and
                   operator_stack.top() in precedence and
                   (precedence[operator_stack.top()] > precedence[token] or
                    (precedence[operator_stack.top()] == precedence[token] and token not in right_associative))):
                output.append(operator_stack.pop())
            operator_stack.push(token)

        else:
            return None, f"Error: invalid token '{token}'"

        i += 1

    while not operator_stack.is_empty():
        op = operator_stack.top()
        if op in '()':
            return None, "Error: mismatched parentheses"
        output.append(operator_stack.pop())

    return ' '.join(output), None


def calculate_postfix(postfix):
    stack = Stack()
    tokens = postfix.split()

    for token in tokens:
        if token.replace('.', '', 1).replace('-', '', 1).isdigit():
            stack.push(float(token))
        elif token in ['+', '-', '*', '/', '**']:
            if stack.size < 2:
                return None, "Error: insufficient operands"
            b = stack.pop()
            a = stack.pop()
            try:
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if abs(b) < 1e-10:
                        return None, "Error: division by zero"
                    result = a / b
                elif token == '**':
                    result = a ** b
                stack.push(result)
            except OverflowError:
                return None, "Error: result too large"
        else:
            return None, f"Error: invalid token '{token}'"

    if stack.size != 1:
        return None, "Error: too many operands"
    result = stack.pop()
    return int(result) if result == int(result) else result, None


def calculate(expression):
    postfix, error = infix_to_postfix(expression)
    if error:
        print(error)
        return
    print(postfix)
    result, error = calculate_postfix(postfix)
    if error:
        print(error)
    else:
        print(result)


# Ввод
try:
    expression = input().strip()
    calculate(expression)
except Exception as e:
    print("Error: invalid input")
