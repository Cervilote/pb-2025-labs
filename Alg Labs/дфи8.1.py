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


def search(root, key, count=0):
    count += 1  # Первое сравнение: с текущим узлом

    if root is None:
        return None, count

    if root.key == key:
        return root, count

    count += 1
    if key < root.key:
        return search(root.left, key, count)
    else:
        return search(root.right, key, count)

def inorder(root):
    result = []
    if root:
        result.extend(inorder(root.left))
        result.append(root.key)
        result.extend(inorder(root.right))
    return result

def preorder(root):
    result = []
    if root:
        result.append(root.key)
        result.extend(preorder(root.left))
        result.extend(preorder(root.right))
    return result

def postorder(root):
    result = []
    if root:
        result.extend(postorder(root.left))
        result.extend(postorder(root.right))
        result.append(root.key)
    return result

def tree_height(root):
    if root is None:
        return 0

    queue = deque([root])
    height = 0

    while queue:
        height += 1  # Увеличиваем счётчик уровней
        level_size = len(queue)

        # Обрабатываем все узлы текущего уровня
        for _ in range(level_size):
            node = queue.popleft()
            # Добавляем потомков в очередь для следующего уровня
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return height
# Создаём дерево: вставляем ключи 50, 30, 70, 20, 40, 60, 80
root = None
keys = [50, 30, 70, 20, 40, 60, 80]
for key in keys:
    root = insert(root, key)

result, comparisons = search(root, 40)
# Поиск
print("Поиск 40:", search(root, 40) is not None)  # True
print("Поиск 25:", search(root, 25) is not None)  # False

# Обходы
print("Inorder:", inorder(root))      # [20, 30, 40, 50, 60, 70, 80]
print("Preorder:", preorder(root))     # [50, 30, 20, 40, 70, 60, 80]
print("Postorder:", postorder(root))   # [20, 40, 30, 60, 80, 70, 50]
print(tree_height(root))