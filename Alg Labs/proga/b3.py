def sift_up(arr,i):
    while i>0:
        parent = (i-1)//2
        if arr[parent] < arr[i]:
            arr[i], arr[parent] = arr[parent], arr[i]
            i=parent
        else:
            break
with open('heapsort.in') as f:
    n= int(f.read())
heap = []
for val in list(range(2,n+1))+[1]:
    heap.append(val)
    sift_up(heap,len(heap)-1)

with open('heapsort.out','w') as f:
    print(*heap, file=f)