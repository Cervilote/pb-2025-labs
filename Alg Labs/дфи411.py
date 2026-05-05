from traceback import print_tb


def bubbleSort(arr):
    c=0
    for i in range(s):
        wasSwapped = False
        c+=1
        for j in range(s - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                wasSwapped = True
        if not wasSwapped:
            break

    return arr,c
s=int(input())
print(bubbleSort([int(i) for i in input().split()]))