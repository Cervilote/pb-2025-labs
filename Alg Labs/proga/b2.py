from fileinput import close

#a=int(input())
#arr=[int(x) for x in input().split()]

with open("input.txt",'r',encoding='utf-8') as f:
    lines = f.readlines()
    a=int(lines[0])
    arr=list(map(int,lines[1].split()))
fo = open('output.txt', 'w', encoding='utf-8')

def counting(arr):
    min=-1000
    ar = [0] * (max(arr) - min + 1)
    for i in arr:
        ar[i - min] += 1
    for i in range(len(ar)):
        if ar[i] > 0:
            #print(i+min(arr), ar[i])
            print(i+min, ar[i], file=fo)

counting(arr)

fo.close()