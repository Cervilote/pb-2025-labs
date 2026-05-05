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


class LinkedList:
    def __init__(self, max_size):
        self.head = None
        self.size = 0
        self.max_size = max_size

    def append(self, item):
        new_node = Node(item)
        if self.size == self.max_size:
            if self.size == 0:
                return
            # Удаляем последний элемент
            if self.head.next is None:
                self.head = None
            else:
                current = self.head
                while current.next.next:
                    current = current.next
                current.next = None
            self.size -= 1
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


class PostfixCalculator:
    def __init__(self, history_size):
        self.history = LinkedList(history_size)

    def evaluate(self, expression):
        stack = Stack()
        tokens = expression.split()

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                stack.push(float(token))
            elif token in ['+', '-', '*', '/', '**']:
                if stack.size < 2:
                    print("Error: insufficient operands")
                    return
                b = stack.pop()
                a = stack.pop()
                try:
                    if token == '+':
                        res = a + b
                    elif token == '-':
                        res = a - b
                    elif token == '*':
                        res = a * b
                    elif token == '/':
                        if abs(b) < 1e-10:
                            print("\nError: division by zero")
                            return
                        res = a / b
                    elif token == '**':
                        res = a ** b
                    stack.push(res)
                except OverflowError:
                    print("Error: result too large")
                    return
            else:
                print(f"Error: invalid token '{token}'")
                return

        if stack.size != 1:
            print("Error: too many operands")
            return

        result = stack.pop()
        result = int(result) if result == int(result) else result
        print(result)
        self.history.append((expression, result))

    def get_history(self):
        return self.history.to_list()

    def undo(self):
        if self.history.size == 0:
            return
        if self.history.size == 1:
            self.history.head = None
            self.history.size = 0
            return
        current = self.history.head
        while current.next.next:
            current = current.next
        current.next = None
        self.history.size -= 1


try:
    k = int(input().strip())
    n = int(input().strip())

    calc = PostfixCalculator(history_size=k)

    for _ in range(n):
        expr = input().strip()
        calc.evaluate(expr)


    history_list = calc.get_history()
    print(history_list)


    calc.undo()
    print("After undo:")
    print(calc.get_history())

except Exception as e:
    print("Error: invalid input")