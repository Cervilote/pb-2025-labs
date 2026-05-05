n = int(input())
segments = []

for _ in range(n):
    left, right = map(int, input().split())
    segments.append((left, right))

def bubble_sort(segments):
    count = len(segments)
    for i in range(count):
        for j in range(count - 1 - i):
            curr = segments[j]
            nxt  = segments[j + 1]
            if curr[0] > nxt[0] or (curr[0] == nxt[0] and curr[1] < nxt[1]):
                segments[j], segments[j + 1] = nxt, curr

bubble_sort(segments)

for left, right in segments:
    print(left, right)