# -*- coding: utf-8 -*-
import re
import sys
import time

sys.setrecursionlimit(10 ** 6)

# () 및 괄호 안 내용 삭제, 특수문자 모두 제거 함수
def clean_text(input_string):
    #() 및 괄호 안 내용 삭제
    regex = "\(.*\)|\s-\s.*"
    text_rmv = re.sub(regex, '', input_string)
    #특수 문자 제거
    text_rmv = re.sub('[^A-Za-z0-9가-힣 ]', '', text_rmv)
    return text_rmv

start = time.time()

file1 = open("1분_target.txt","r",encoding='UTF8')
file2 = open("1분_test.txt","r",encoding='UTF8')

T_target = clean_text(file1.read()).splitlines()
T_test = clean_text(file2.read()).splitlines()

T_list_output = [] 

# 기본적으로 ( , 2)을 넣어서 삭제된 것 출력되도록 준비 
inner = []
inner_tmp = []

for i,a in enumerate(T_target):
    num = 0
    for b in a:
        inner_tmp.append([b, 2])
        num = num + 1
    inner = inner_tmp.copy()
    T_list_output.append(inner)
    inner_tmp.clear()

tmp = []
output = []
count = 0

# 함수 정의
'''
P : 패턴
T : 텍스트
S : Start
'''
def JJJ(P,T,S):
    m = len(P)
    check = 0
    # S > len(target) - len(패턴) + 1이면 비교 중단
    if S < len(T) - len(P) + 1:
        while check == 0:
            #중복걸러주는 코드 - 불안정
            if T_list_output[global_i][S][1] == 1:
                S += 1
                continue 
            # P[0]과 T[i] 비교하며 시작 (Compare leftmost)
            if P[0] != T[S] :
                # leftmost 비교 /  alphabet-alphabet MisMatch case
                if T[S].isalpha():
                    S = S + 2 # 두 칸 이동
                    return JJJ(P,T,S)
                # leftmost 비교 / alphabet-blank MisMatch case
                else:
                    S = S + 1 # 한 칸 이동
                    return JJJ(P,T,S)
            # leftmost Compare Success
            else:
                m_tmp = m
                # Compare rightmost
                # 한글자짜리 걸러내기
                if m==1:
                    check = 2
                    T_list_output[global_i][S] = [T[S],1]
                    S = (len(T)-1)
                elif P[m_tmp-1] == T[S+m_tmp-1]:
                    # 남은 패턴 문자 비교
                    for _ in range(m):
                        # 다르면
                        if P[m_tmp-2] != T[S+m_tmp-2]:
                            S = S + m
                            break
                        m_tmp -= 1
                        # 다 같으면
                        if m_tmp == 1:
                            # ( ,1) = 흰색
                            for j in range(S,S+m):
                                T_list_output[global_i][j] = [T[j],1]                
                                S = (len(T)-1) #while문 종료를 위해
                            check = 2
                            break
                # rightmost mismatch
                else:
                    # leftmost 매치 OK / rightmost 매치 FAIL / alphabet-alphabet
                    if T[S+m-1].isalpha():
                        if T[S+(m)] == ' ':
                            S = S+m+1
                            return JJJ(P,T,S)
                        else:
                            S = S+2
                            return JJJ(P,T,S)
                    # leftmost 매치 OK / rightmost 매치 FAIL / alphabet-blank 
                    else:
                        # 패턴길이만큼 오른쪽 이동
                        S = S+m
                        return JJJ(P,T,S)
    else:
        if check == 0 :
            # (,3) 매칭 제로 -> 추가된 것이라 파란색으로
            tmp.append([P,global_i])
        else: # 매칭이 됐던 거라서 재끼기
            return

# 실행 부분
idx1 = 0
P_list = []
for x in T_test:
    P_list.append(x.split())
    idx1 = idx1 + 1

global global_i
for global_i,x in enumerate(T_target):
    for z in P_list[global_i]:
        JJJ(z,x,0)

#print(tmp)
for i,r in enumerate(tmp):
    for s in re.finditer(r[0],T_test[r[1]]):
        if T_list_output[r[1]][s.start()] == ' ':
            T_list_output[r[1]].insert(s.start()+1,[r[0],3])
        else:
            T_list_output[r[1]].insert(s.start(),[r[0],3])

#print(T_list_output)
print("비교 : ",end='')
for q in T_list_output:
    for r in q:        
        if r[1] == 1: # 하얀색
            print(r[0], end='')
        elif r[1] == 2: # 빨간색
            print('\033[31m'+r[0]+'\033[0m', end= '')
        else:         # 파란색
            print('\033[34m'+r[0]+'\033[0m', end =' ')

print(time.time()-start)