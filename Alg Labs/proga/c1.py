from unittest import result

inpu, output = map(str, input().split())

def EdgeToMat():
    for _ in range(e_count):
        a, b = map(int, input().split())
        mx[a][b] = 1
    print(v_count)
    for i in range(1, v_count + 1):
        print(*mx[i][1:v_count + 1])

def EdgeToList():
    for _ in range(e_count):
        a, b = map(int, input().split())
        lst[a].append(b)
    print(v_count)
    for key, value in lst.items():
        print(len(value), *value)

def MatToList():
    for i in range(v_count):
        n=list(map(int,input().split()))
        lst[i+1]=[j+1 for j in range(len(n)) if n[j]==1]
    print(v_count)
    for key, value in lst.items():
        print(len(value), *value)

def MatToEdge():
    result=[]
    for i in range(v_count):
        n=list(map(int,input().split()))
        for j in range(len(n)):
            if n[j]==1:
                result.append([i+1,j+1])
    print(v_count,len(result))
    for item in result:
        print(*item)

def ListToMat():
    print(v_count)
    for i in range(v_count):
        sroka=[0]*v_count
        n=list(map(int,input().split()))
        if n!=[0]:
            n.pop(0)
            for item in n:
                sroka[item-1]=1
            print(*sroka)
        else:
            print(*sroka)

def ListToEdges():
    result=[]
    for i in range(v_count):
        sroka=[0]*v_count
        n=list(map(int,input().split()))
        if n!=[0]:
            n.pop(0)
            for j in n:
                result.append([i+1,j])
    print(v_count,len(result))
    for items in result:
        print(*items)




if inpu=='edges' and output=='mat':
    v_count, e_count = map(int, input().split())
    mx = [[0] * (v_count + 1) for _ in range(v_count + 1)]
    EdgeToMat()

if inpu=='edges' and output=='lists':
    v_count, e_count = map(int, input().split())
    lst = {i: [] for i in range(1, v_count + 1)}
    EdgeToList()

if inpu=='mat' and output=='lists':
    v_count=(int(input()))
    lst = {i: [] for i in range(1, v_count + 1)}
    MatToList()

if inpu=='mat' and output=='edges':
    v_count = int(input())
    MatToEdge()

if inpu=='lists' and output=='mat':
    v_count= int(input())
    ListToMat()

if inpu=='lists' and output=='edges':
    v_count = int(input())
    ListToEdges()