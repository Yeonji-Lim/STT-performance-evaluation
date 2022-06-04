from pprint import pprint

s1 = "가 나 다 라 마 바 사 아 자 차 카"
s2 = "가 나 라 라 마 하 사 아 타 파 차 카"


list1 = s1.split(" ")
n1 = len(list1)
list2 = s2.split(" ")
n2 = len(list2)



dp = [[0] * (n2+1) for _ in range(n1+1)]

for i in range(1, n1+1):
    for j in range(1, n2+1):
        if list1[i-1] == list2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i][j-1], dp[i-1][j])
print(dp[-1][-1])


lenResult = n1+n2-dp[-1][-1]
matrix = [[0 for col in range(lenResult)] for row in range(2)]

a = n1
b = n2
tranLen = lenResult

while tranLen > 0:
    if a == 0 or b == 0:
        break
    if dp[a][b] == dp[a-1][b]:
        matrix[0][tranLen - 1] = list1[a - 1]
        matrix[1][tranLen - 1] = -1
        tranLen -= 1
        a -= 1
    elif dp[a][b] == dp[a][b-1]:
        matrix[0][tranLen - 1] = list2[b - 1]
        matrix[1][tranLen - 1] = 1
        tranLen -= 1
        b -= 1
    else:
        matrix[0][tranLen - 1] = list1[a - 1]
        matrix[1][tranLen - 1] = 0
        tranLen -= 1
        a -= 1
        b -= 1

number = 0
for t in matrix[0]:
    if matrix[1][number] == 0:
        number += 1
        print(t + ' ', end='')
    elif matrix[1][number] == 1:
        number += 1
        print('\033[34m' + t + ' ', end='' + '\033[0m')
    else:
        number += 1
        print('\033[31m' + t + ' ', end='' + '\033[0m')








