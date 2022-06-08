from multiprocessing import freeze_support
import kss
import re
import algorithm1

# () 및 괄호 안 내용 삭제, 특수문자 모두 제거
def clean_text(input_string):
    regex = "\(.*\)|\s-\s.*"
    text_rmv = re.sub(regex, '', input_string)
    text_rmv = re.sub('[^A-Za-z0-9가-힣 ]', '', text_rmv)
    return text_rmv

# txt파일 일기
f1 = open("test.txt", "r", encoding='UTF8')
f2 = open("target.txt", "r", encoding='UTF8')

# 줄바꿈 삭제
s1 = f1.read().replace("\n", " ")
s2 = f2.read().replace("\n", " ")

s1 = clean_text(s1)
s2 = clean_text(s2)

list_a = []
list_b = []

# 문장 분할
if __name__ == '__main__':
    freeze_support()
    for sent1 in kss.split_sentences(s1):
        list_a.append(sent1)
    for sent2 in kss.split_sentences(s2):
        list_b.append(sent2)

    n1 = len(list_a)
    n2 = len(list_b)

    if n1!=n2:
        print("error")
    else:
        num = 0
        while num < n1:
            algorithm1.lcs(list_a[num], list_b[num])
            num += 1


# 읽기 종료
f1.close()
f2.close()

