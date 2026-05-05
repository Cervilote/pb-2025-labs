import heapq

with open('input.txt','r') as f:
    lines = f.readlines()
    n,k = map(int,lines[0].split())
    arr = list(map(int,lines[1].split()))

arr= [(arr[i],i) for i in range(n)]
heapq.heapify(arr)
last_index = n-1

for _ in range(k):
    s1 = heapq.heappop(arr)[0]
    s2 = heapq.heappop(arr)[0]

    last_index +=1
    heapq.heappush(arr,(s1 + s2,last_index))
with open('output.txt','w') as fo:
    for (elem, index) in sorted(arr, key=lambda x:x[1]):
        print(elem,end=' ',file=fo)
