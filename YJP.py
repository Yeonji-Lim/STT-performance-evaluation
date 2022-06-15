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
        # 해시 값 계산
        hash = 0
        for i in range(len(word_byte)):
            hash = (word_byte[i]+hash) % len(table)
        # 해시 값으로 매핑
        table[hash].append(Node(word, index))

# 단어 배열(words)에서 단어(word) 찾기
def findWord(words, word):
    for i, target in enumerate(words):
        if target == word:
            return i
    return -1 # 찾지 못한 경우 -1 반환

def YJP(target, test):
    result_words = []               # 결과 단어 배열
    target_words = target.split()   # 타깃 단어 배열
    test_words = test.split()       # 테스트 단어 배열

    # 타깃 단어 배열의 원소수가 0인 경우 : 타깃 문자열이 빈 문자열
    if len(target_words) == 0:
        # 테스트에만 있는 단어
        for word in test_words:
            result_words.append(testOnly(word))
        # 결과 반환
        result = " ".join(result_words)
        return result
    
    # 테스트 단어 배열의 원소수가 0인 경우 : 테스트 문자열이 빈 문자열
    if len(test_words) == 0:
        # 타깃에만 있는 단어
        for word in target_words:
            result_words.append(targetOnly(word))
        # 결과 반환
        result = " ".join(result_words)
        return result

    # 테스트와 타깃 모두 단어가 한 개인 경우 : 각 단어만을 비교
    if len(target_words) == 1 and len(test_words) == 1:
        if target_words[0] == test_words[0]:
            result_words.append(target_words[0])
        else:
            result_words.append(targetOnly(target_words[0]))
            result_words.append(testOnly(test_words[0]))
        # 결과 반환
        result = " ".join(result_words)
        return result

    # 각 텍스트에 대응하는 테이블 
    table_size = 997
    target_table = [[] for _ in range(table_size)]
    test_table = [[] for _ in range(table_size)]

    # 해시 테이블 매핑
    mappingTable(target_table, target_words)
    mappingTable(test_table, test_words)

    # 타깃 해시 테이블의 각 버킷의 원소수를 (해시값, 버킷의 원소수)로 target_arr에 저장
    target_arr = []
    for i in range(table_size):
        if len(target_table[i]) != 0 and len(test_table[i]) != 0:
            target_arr.append((i, len(target_table[i])))  # (해시값, 버킷의 원소수)

    # 버킷의 원소수가 작을 수록, 테스트 테이블의 원소 개수가 작을 수록 앞으로 오게 정렬
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

    # target_arr를 정렬
    target_arr = merge_sort(target_arr)
    
    # 앞선 unique_word의 인덱스를 저장할 우선 순위 큐
    target_vq = PriorityQueue()
    test_vq = PriorityQueue()

    # 정렬된 target_arr는 그 앞에 unique_word의 해시값이 오도록 정렬되어 있다.
    for hash, num in target_arr:
        # 버킷의 원소수가 1개가 아니면 break
        if num != 1 :
            break
        
        # 실제로 단어가 같다면
        if target_table[hash][0].word == test_table[hash][0].word:
            # 해당 단어의 각 데이터에서의 인덱스
            target_idx = target_table[hash][0].index
            test_idx = test_table[hash][0].index
            # 각 데이터에서의 구간 
            target_range = [target_idx, target_idx]
            test_range = [test_idx, test_idx]
            # 구간 체크 : 가장 가까운 unique_word의 구간 범위
            if not target_vq.empty() and not test_vq.empty(): # 기존에 발견한 unique_word가 있는 경우
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
            # 동일 구간 여부 체크 : 구간의 끝 인덱스 값의 단어가 서로 같으면
            if target_words[target_range[0]] == test_words[test_range[0]] and \
               target_words[target_range[1]] == test_words[test_range[1]]:
                # unique_word로 간주, 우선순위 큐에 삽입
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

    # 남은 구간에 대해서 재귀 진행 : 큐에 들어있지 않은 인덱스 구간
    prei = -1
    prej = -1
    i = target_vq.get()
    j = test_vq.get()
    while i < len(target_words) and j < len(test_words):
        # i, j 모두 직전 인덱스와 같다면 다음 단어로 진행
        if i == prei+1 and j == prej+1:
            result_words.append(target_words[i])
            prei = i
            prej = j
            if target_vq.empty() or test_vq.empty(): break
            i = target_vq.get()
            j = test_vq.get()
            continue
        # 남은 구간 발생
        new_target = ""
        new_test = ""
        for k in range(prei+1, i):
            new_target += target_words[k]+' '
        for k in range(prej+1, j):
            new_test += test_words[k]+' '
        # 다시 YJP 진행 후 결과 리스트에 추가
        result_words.append(YJP(new_target, new_test).rstrip())
        # 다음 반복에서 직전 인덱스와 같도록 수정
        prei = i-1
        prej = j-1

    # 남은 뒷 부분 문자열에 대해서 YJP 진행
    new_target = ""
    new_test = ""
    for k in range(i+1, len(target_words)):
        new_target += target_words[k]+" "
    for k in range(j+1, len(test_words)):
        new_test += test_words[k]+" "
    result_words.append(YJP(new_target, new_test).rstrip())
    
    # 결과 반환
    result = " ".join(result_words)
    return result

# 알고리즘 시작 시간
start = time.time()

target = clean_text(open("1분_target.txt", 'r').read())
test = clean_text(open("1분_test.txt", 'r').read())

# 결과 출력
print(YJP(target, test))

# 소요시간 체크
print(time.time()-start)