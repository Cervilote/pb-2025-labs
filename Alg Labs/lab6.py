# class Stack:
#     def __init__(self):
#         self.items = []
#         self.top_index = -1
#
#     def push(self, item):
#         self.items.append(item)
#         self.top_index += 1
#
#     def pop(self):
#         if self.is_empty():
#             return None
#         self.top_index -= 1
#         return self.items.pop()
#
#     def top(self):
#         if self.is_empty():
#             return None
#         return self.items[self.top_index]
#
#     def is_empty(self):
#         return self.top_index == -1
#
#
# def is_correct_brackets(s):
#     stack = Stack()
#     for char in s:
#         if char == '(':
#             stack.push(char)
#         elif char == ')':
#             if stack.is_empty():
#                 return 'NO'
#             stack.pop()
#     return 'YES' if stack.is_empty() else 'NO'
#
#
# s = input().strip()
# print(is_correct_brackets(s))

class HashTable:
    def __init__(self, size=11):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self._hash(key)
        chain = self.table[index]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))

    def search(self, key):
        index = self._hash(key)
        chain = self.table[index]
        for k, v in chain:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        chain = self.table[index]
        for i, (k, v) in enumerate(chain):
            if k == key:
                del chain[i]
                return True
        return False

    def display(self):
        arr=[]
        for i in range(self.size):
            chain = self.table[i]
            arr.append(chain)
        return arr


n = int(input())

ht = HashTable()


for _ in range(n):
    key, value = map(int, input().split())
    ht.insert(key, value)

x = int(input())
y = int(input())
d = int(input())


print(ht.search(x))
print(ht.search(y))
print(ht.delete(d))
print(ht.display())
