from LinkedList import LinkedList
from Dic import Dic

target_file = open("target.txt", 'r')
test_file = open("test.txt", 'r')

# target = target_file.read()
# test = test_file.read()

target_words = target_file.read().split()
test_words = test_file.read().split()

# test = '힣'
# test_byte = test.encode('utf-8')

# for i in range(len(test_byte)):
#     print(test_byte[i])

# value = 0
# for i in range(len(test_byte)) :
#     print(test_byte[i])
#     value += test_byte[i]
# print("value = ",value)

table_size = 4000
table = Dic(table_size)

for word in target_words :
    # print(word)
    word_byte = word.encode('utf-8')
    hash = 0
    for i in range(len(word_byte)) :
        hash = (word_byte[i]+hash) % table_size
    #print(hash)

    # 단어 해시 값 테이블에 매핑
    table.add(hash, word)
    # table.print()

table.print()

# TODO : 그 중 버킷에 적은 원소가 들어간 단어 선택 -> 해당 단어의 인덱스 기억해야 함

# TODO : 그 단어를 test에서 찾음 -> 이것도 인덱스 기억
# 그런데 이 단어가 test에서 2개 이상 이면..? -> 다른 unique word 탐색? || 그냥 앞에 걸로 진행 || 가장 가까운 인덱스 선택(이게 맞을 듯)

# TODO : 그 단어를 기준으로 target과 test를 앞뒤로 다시 나눠서 똑같은 과정 진행 
# -> 인덱스를 해시 테이블에 넣을 때 같이 포함해서 넣음, 다음 unique word를 뽑을 때 인덱스 범위가 지금 나뉜 범위와 맞지 않으면 패스
