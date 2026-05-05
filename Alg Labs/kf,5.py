class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def add_first(self,data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.data, end=" → ")
            current = current.next
        print('None')

    def add_last(self,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def remove(self,data):
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            return True

        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def add(self,pos,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        if pos == 0:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        count = 0
        while current and count < pos-1:
            count += 1
            current = current.next

        if current is None:
                ss.add_last(data)

        else:
            new_node.next = current.next
            current.next = new_node

    def arr(self):
        arr=[]
        current = self.head
        while current is not None:
            arr.append(current.data)
            current = current.next
        return arr

    def leen(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def find(self,data):
        count = 0
        current = self.head
        while current:
            if current.data == data:
                return count
            count += 1
            current = current.next
        return -1

#n = int(input())
#numbers = list(map(int, input().split()))
#x = int(input())
#y = int(input())
ss= LinkedList()

n = int(input())
numbers = list(map(int, input().split()))
pos,val = map(int, input().split())
dele = int(input())
for i in range(n):
    ss.add_last(numbers[i])
#for i in range(n):
#    ss.add_first(numbers[i])
#ss.print_list()
#print(ss.leen())
#print(ss.find(x))
#print(ss.find(y))


ss.add(pos,val)
ss.print_list()
print(ss.remove(dele))
ss.print_list()
print(ss.arr())
