from queue import PriorityQueue

class Node:
    def __init__(self, word=None, index=None):
        self.word = word
        self.index = index

def mappingTable(table, words):
    for index, word in enumerate(words):
        word_byte = word.encode('utf-8')
        hash = 0
        for i in range(len(word_byte)):
            hash = (word_byte[i]+hash) % len(table)
        table[hash].append(Node(word, index))

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
            result_words.append('\033[34m' + word + '\033[0m')
        result = " ".join(result_words)
        return result
    
    if len(test_words) == 0:
        for word in target_words:
            result_words.append('\033[31m' + word + '\033[0m')
        result = " ".join(result_words)
        return result

    if len(target_words) == 1 and len(test_words) == 1:
        if target_words[0] == test_words[0]:
            result_words.append(target_words[0])
        else:
            result_words.append('\033[31m' + target_words[0] + '\033[0m')
            result_words.append('\033[34m' + test_words[0] + '\033[0m')
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

    # for i in range(len(target_arr)):
    #     print(target_arr[i][0], target_arr[i][1])
    
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

    if target_vq.empty():
        for word in test_words:
            idx = findWord(target_words, word)
            if idx == -1:
                result_words.append('\033[34m'+ word +'\033[0m')
            else:
                for i in range(idx):
                    result_words.append('\033[31m'+ target_words[i] +'\033[0m')
                    del target_words[i]
                result_words.append(target_words[0])
                del target_words[0]
        for word in target_words:
            result_words.append('\033[31m'+ word +'\033[0m')
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

target = open("data/알고리즘강의_target.txt", 'r').read()
test = open("data/알고리즘강의_test.txt", 'r').read()

print(patience(target, test))
