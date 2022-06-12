# lcs 알고리즘
def lcs(str1, str2):
    # 문장을 단어로 분리
    list1 = str1.split()
    list2 = str2.split()

    # 단어수 세기
    n1 = len(list1)
    n2 = len(list2)

    # 2차원 배열 생성(앞 마진 = 0)
    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            #두 단어가 같으면 dp[i-1][j-1]+1 대입
            if list1[i - 1] == list2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            # 두 단어가 다르면 dp[i-1][j]와 dp[i][j-1]중 큰값을 대입
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
    
    # 최장 공통 단어 수 출력
    # print(dp[-1][-1])

    # (list1 단어수 + list2 단어수) - (공통된 단어수)
    lenResult = n1 + n2 - dp[-1][-1]
    # 2차원 배열 생성(1행:단어, 2행:공통(0)/삭제(-1)/삽입(1))
    matrix = [[0 for col in range(lenResult)] for row in range(2)]

    while lenResult > 0:
        # 배열 값이 0인지 확인
        if dp[n1][n2] == 0:
            # n2가 0보가 크고 남은 배열 길이가 0보다 크면
            while n2 > 0 and lenResult > 0:
                # 문자열 배열에 추가된 문자열 추가
                matrix[0][lenResult - 1] = list2[n2 - 1]
                matrix[1][lenResult - 1] = 1
                lenResult -= 1
                n2 -= 1
            # n1가 0보가 크고 남은 배열 길이가 0보다 크면
            while n1 > 0 and lenResult > 0:
                # 문자열 배열에  삭제된 문자열 추가
                matrix[0][lenResult - 1] = list1[n1 - 1]
                matrix[1][lenResult - 1] = -1
                lenResult -= 1
                n1 -= 1
        # DP[i][j]와 DP[i][j-1]이 같을 때 추가된 단어 추가 
        elif dp[n1][n2] == dp[n1][n2 - 1]:
            matrix[0][lenResult - 1] = list2[n2 - 1]
            matrix[1][lenResult - 1] = 1
            lenResult -= 1
            n2 -= 1
        # DP[i][j]와 DP[i-1][j]이 같을 때 삭제된 단어 추가
        elif dp[n1][n2] == dp[n1 - 1][n2]:
            matrix[0][lenResult - 1] = list1[n1 - 1]
            matrix[1][lenResult - 1] = -1
            lenResult -= 1
            n1 -= 1
        # DP[i][j]와 DP[i-1][j],DP[i][j-1]이 다를 때 공통 단어 추가
        else:
            matrix[0][lenResult - 1] = list1[n1 - 1]
            matrix[1][lenResult - 1] = 0
            lenResult -= 1
            n1 -= 1
            n2 -= 1

    # 문자열 출력
    number = 0
    for t in matrix[0]:
        # 0이면 그냥 문자열 출력
        if matrix[1][number] == 0:
            number += 1
            print(t, end=' ')
        # 1이면 파란색으로 문자열 출력
        elif matrix[1][number] == 1:
            number += 1
            print('\033[34m' + t + '\033[0m', end=' ')
        # -1이면 빨간색으로 문자열 출력
        else:
            number += 1
            print('\033[31m' + t + '\033[0m', end=' ')
