#
# bucket = [[] for _ in range(10)]
# temp = []
#
# # 123 % 10^1 // 10^0
# # 123 % 10^2 // 10^1
# # 123 % 10^3 // 10^2
# for i in range(4):
#     for elem in arr:
#         bucket[elem % 10 ** (i + 1) // 10 ** i].append(elem)
#     for b_ind in range(10):
#         temp.extend(bucket[b_ind])
#         bucket[b_ind] = []
#     arr = temp
#     temp = []
# print(arr)



with open('input.txt', 'r') as f:
    lines = f.readlines()
    n = int(lines[0])
    words = [line.strip() for line in lines[1:n + 1]]

for pos in range(2, -1, -1):
    bucket = [[] for _ in range(128)]

    for word in words:
        bucket[ord(word[pos])].append(word)

    words = [word for bucket_list in bucket for word in bucket_list]

with open('output.txt', 'w') as fo:
    fo.write('\n'.join(words) + '\n')

