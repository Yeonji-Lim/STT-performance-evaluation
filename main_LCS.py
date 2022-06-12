import re
import time
import LCS

# () 및 괄호 안 내용 삭제, 특수문자 모두 제거 함수
def clean_text(input_string):
    #() 및 괄호 안 내용 삭제
    regex = "\(.*\)|\s-\s.*"
    text_rmv = re.sub(regex, '', input_string)
    #특수 문자 제거
    text_rmv = re.sub('[^A-Za-z0-9가-힣 ]', '', text_rmv)
    return text_rmv

start = time.time()

# txt파일 일기
f1 = open("target.txt", "r", encoding='UTF8')
f2 = open("test.txt", "r", encoding='UTF8')

# 줄바꿈 삭제
s1 = f1.read().replace("\n", " ")
s2 = f2.read().replace("\n", " ")

#특수문자 제거 
s1 = clean_text(s1)
s2 = clean_text(s2)

LCS.lcs(s1,s2)

print(time.time()-start)

# 읽기 종료
f1.close()
f2.close()
