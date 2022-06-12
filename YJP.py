from queue import PriorityQueue
import re
import time

# 파란 글씨 : 테스트에만 있는 단어
def testOnly(word):
    return '\033[34m' + word + '\033[0m'

# 빨간 글씨 : 타깃에만 있는 단어
def targetOnly(word):
    return '\033[31m' + word + '\033[0m'

# () 및 괄호 안 내용 삭제, 특수문자 모두 제거 함수
def clean_text(input_string):
    #특수 문자 제거
    text_rmv = re.sub('[^A-Za-z0-9가-힣 ]', '', input_string)
    return text_rmv

# 버킷에 들어가는 노드
class Node:
    def __init__(self, word=None, index=None):
        self.word = word
        self.index = index

# 해시 테이블 매핑
def mappingTable(table, words):
    for index, word in enumerate(words):
        # utf-8 인코딩으로 바꿔주기
        word_byte = word.encode('utf-8')
        # 
        hash = 0
        for i in range(len(word_byte)):
            hash = (word_byte[i]+hash) % len(table)
        table[hash].append(Node(word, index))

# 단어 배열에서 단어 찾기
def findWord(words, word):
    for i, target in enumerate(words):
        if target == word:
            return i
    return -1

def patience(target, test):
    result_words = []
    target_words = target.split()
    test_words = test.split()

    if len(target_words) == 0:
        for word in test_words:
            result_words.append(testOnly(word))
        result = " ".join(result_words)
        return result
    
    if len(test_words) == 0:
        for word in target_words:
            result_words.append(targetOnly(word))
        result = " ".join(result_words)
        return result

    if len(target_words) == 1 and len(test_words) == 1:
        if target_words[0] == test_words[0]:
            result_words.append(target_words[0])
        else:
            result_words.append(targetOnly(target_words[0]))
            result_words.append(testOnly(test_words[0]))
        result = " ".join(result_words)
        return result

    table_size = 997
    target_table = [[] for _ in range(table_size)]
    test_table = [[] for _ in range(table_size)]

    mappingTable(target_table, target_words)
    mappingTable(test_table, test_words)

    target_arr = []
    for i in range(table_size):
        if len(target_table[i]) != 0 and len(test_table[i]) != 0:
            target_arr.append((i, len(target_table[i])))  # (해시값, 버킷의 원소수)

    def merge_sort(arr):
        if len(arr) < 2:
            return arr

        mid = len(arr) // 2
        low_arr = merge_sort(arr[:mid])
        high_arr = merge_sort(arr[mid:])

        merged_arr = []
        l = h = 0
        while l < len(low_arr) and h < len(high_arr):
            if low_arr[l][1] < high_arr[h][1]:
                merged_arr.append(low_arr[l])
                l += 1
            elif low_arr[l][1] > high_arr[h][1]:
                merged_arr.append(high_arr[h])
                h += 1
            # 테이블 원소의 개수가 같은 경우에는 테스트 테이블의 원소 개수를 비교
            elif len(test_table[low_arr[l][0]]) < len(test_table[high_arr[h][0]]):
                merged_arr.append(low_arr[l])
                l += 1
            else:
                merged_arr.append(high_arr[h])
                h += 1

        merged_arr += low_arr[l:]
        merged_arr += high_arr[h:]
        return merged_arr

    target_arr = merge_sort(target_arr)
    
    target_vq = PriorityQueue()
    test_vq = PriorityQueue()
    for hash, num in target_arr:
        if num != 1 :
            break
        
        if target_table[hash][0].word == test_table[hash][0].word:
            target_idx = target_table[hash][0].index
            test_idx = test_table[hash][0].index
            target_range = [target_idx, target_idx]
            test_range = [test_idx, test_idx]
            # 구간 체크
            if not target_vq.empty() and not test_vq.empty():
                for nodeidx in target_vq.queue:
                    if target_idx < nodeidx:
                        target_range[1] = nodeidx
                        break
                    else:
                        target_range[0] = nodeidx
                for nodeidx in test_vq.queue:
                    if test_idx < nodeidx:
                        test_range[1] = nodeidx
                        break
                    else:
                        test_range[0] = nodeidx
            # 동일 구간 여부 체크
            if target_words[target_range[0]] == test_words[test_range[0]] and \
               target_words[target_range[1]] == test_words[test_range[1]]:
                target_vq.put(target_idx)
                test_vq.put(test_idx)

    # 일치하는 부분이 없는 경우
    if target_vq.empty():
        for word in test_words: # test에 있는 단어 각각에 대해서
            # target에 해당 단어가 있는 지 확인
            idx = findWord(target_words, word)
            if idx == -1: # target에 없는 경우 : test에만 있는 단어
                result_words.append(testOnly(word))
            else:
                # 찾은 단어보다 앞에 있는 target 단어 : target에만 있는 단어 
                while target_words[0] != word: 
                    result_words.append(targetOnly(target_words[0]))
                    # 추가하고 삭제
                    del target_words[0]
                # 남은 가장 앞의 단어가 실제 일치한 단어
                result_words.append(target_words[0])
                # 추가하고 삭제
                del target_words[0]
        # 남은 target 단어 : target에만 있는 단어
        for word in target_words:
            result_words.append(targetOnly(word))
        # 결과 반환
        result = " ".join(result_words)
        return result

    prei = -1
    prej = -1
    i = target_vq.get()
    j = test_vq.get()
    while i < len(target_words) and j < len(test_words):
        if i == prei+1 and j == prej+1:
            result_words.append(target_words[i])
            prei = i
            prej = j
            if target_vq.empty() or test_vq.empty(): break
            i = target_vq.get()
            j = test_vq.get()
            continue
        new_target = ""
        new_test = ""
        for k in range(prei+1, i):
            new_target += target_words[k]+' '
        for k in range(prej+1, j):
            new_test += test_words[k]+' '
        result_words.append(patience(new_target, new_test).rstrip())
        prei = i-1
        prej = j-1

    new_target = ""
    new_test = ""
    for k in range(i+1, len(target_words)):
        new_target += target_words[k]+" "
    for k in range(j+1, len(test_words)):
        new_test += test_words[k]+" "
    result_words.append(patience(new_target, new_test).rstrip())
    
    result = " ".join(result_words)
    return result

start = time.time()

target = clean_text(open("target.txt", 'r').read())
test = clean_text(open("test.txt", 'r').read())

print(patience(target, test))

print(time.time()-start)