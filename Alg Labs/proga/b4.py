import heapq

with open('input.txt', 'r') as file:
    lines=file.readlines()
    n = int(lines[0])
    arr=list(map(int,lines[1].split()))

max_heap = []
min_heap = []
result=[]
with open('output.txt', 'w') as file:
    for num in arr:
        if max_heap and num <= -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)

        if len(max_heap) > len(min_heap)+1:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        elif len(min_heap) > len(max_heap):
            heapq.heappush(max_heap, -heapq.heappop(min_heap))

        result.append(-max_heap[0])
    print(' '.join(map(str, result)),file=file)