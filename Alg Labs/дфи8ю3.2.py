from collections import deque

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

def inorder(root):
    result = []
    if root:
        result.extend(inorder(root.left))
        result.append(root.key)
        result.extend(inorder(root.right))
    return result

def level_order(root):
    """Обход по уровням (BFS)"""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.key)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

def find_min(node):
    while node.left is not None:
        node = node.left
    return node

def delete(root, key):
    if root is None:
        return root
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        # Случай 1: Удаление листа (нет потомков)
        if root.left is None and root.right is None:
            print(f"Удаление листа {key}")
            return None
        # Случай 2: Узел с одним потомком
        elif root.left is None:
            print(f"Удаление узла {key} с одним правым потомком")
            return root.right
        elif root.right is None:
            print(f"Удаление узла {key} с одним левым потомком")
            return root.left
        # Случай 3: Узел с двумя потомками
        else:
            print(f"Удаление узла {key} с двумя потомками")
            successor = find_min(root.right)  # Находим преемника
            root.key = successor.key  # Заменяем значение
            root.right = delete(root.right, successor.key)  # Удаляем преемника
    return root

# Основная программа
keys = [50, 30, 120, 70, 20, 90, 40, 60, 80]
root = None

# Построение дерева
for key in keys:
    root = insert(root, key)

# Вывод начального состояния
print("Initial:")
print("Inorder:", inorder(root))
print("Level-order:", level_order(root))

# Последовательное удаление с выводом
for key_to_delete in [20, 30, 50]:
    print(f"\nAfter delete {key_to_delete}:")
    root = delete(root, key_to_delete)
    print("Inorder:", inorder(root))
    print("Level-order:", level_order(root))
