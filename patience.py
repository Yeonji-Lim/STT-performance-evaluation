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
        # self.print()
        # print()

def findWord(words, word):
    for i, target in enumerate(words):
        if target == word:
            return i
    return -1

def patience(target, test):

    result = ""
    target_words = target.split()
    test_words = test.split()

    if len(target_words) == 0:
        for word in test_words:
            result += '\033[34m' + word + ' \033[0m'
        return result
    
    if len(test_words) == 0:
        for word in target_words:
            result += '\033[31m' + word + ' \033[0m'
        return result

    if len(target_words) == 1 and len(test_words) == 1:
        if target_words[0] == test_words[0]:
            result += target_words[0]
        else:
            result += '\033[31m' + target_words[0] + ' \033[0m' + '\033[34m' + test_words[0] + ' \033[0m'
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

    visited_target = [False for _ in range(len(target_words))]
    visited_test = [False for _ in range(len(test_words))]

    def isAllEqual(bucket):
        firstWord = bucket[0].word
        for node in bucket:
            if node.word != firstWord:
                return False
        return True
    
    leastOneEqual = False
    target_vq = PriorityQueue()
    test_vq = PriorityQueue()
    for hash, num in target_arr:
        # if num != 1:
        #     continue
        
        # if target_words[hash][0].word == test_words[hash][0].word:
        #     target_idx = target_words[hash][0].index
        #     testidx = test_words[hash][0].index
        #     target_range = (0, 0)
        #     test_rage = (0, 0)
        #     if len(target_vq) != 0:
        #         for nodeidx in target_vq:
        #             if target_idx < nodeidx:
        #                 target_range[1] = nodeidx
        #     target_vq.put(target_idx)
        #     test_vq.put(testidx)

        
        # TODO 앞에서 유니크 단어 뽑았던거 기억해두었다가 지금 target과 test의 인덱스가 구간이 안맞으면 pass

        target_bucket = target_table[hash]
        test_bucket = test_table[hash]

        if len(target_bucket) == len(test_bucket) and \
            target_bucket[0].word == test_bucket[0].word:

            if isAllEqual(target_bucket) and isAllEqual(test_bucket): 
                leastOneEqual = True
                for node in target_bucket:
                    visited_target[node.index] = True
                for node in test_bucket:
                    visited_test[node.index] = True
                continue
            
            # 142 우리 112 따라 140
            # 688 정렬이 51 정렬이 148 정렬이 165
            # 688 정렬이 46 정렬이 137 정맥이 153
            for i, node in enumerate(target_bucket) :
                leastOneEqual = True
                if node.word != test_bucket[i].word:
                    break
                visited_target[node.index] = True
                visited_test[test_bucket[i].index] = True

    if not leastOneEqual:
        for word in test_words:
            idx = findWord(target_words, word)
            if idx == -1:
                result += '\033[34m' + word + ' \033[0m'
            else:
                for i in range(idx):
                    result += '\033[31m' + target_words[i] + ' \033[0m'
                    del target_words[i]
                result += target_words[0]+' '
                del target_words[0]
        for word in target_words:
            result += '\033[31m' + word + ' \033[0m'
        return result
            
    i = 0
    j = 0
    while i < len(target_words) and j < len(test_words) :
        if visited_target[i] and visited_test[j]:
            result += target_words[i] + ' '
            i += 1
            j += 1
            continue

        new_target = ""
        new_test = ""
        while i < len(target_words) and not visited_target[i]:
            new_target += target_words[i]+' '
            i+=1
        while j < len(test_words) and not visited_test[j]:
            new_test += test_words[j]+' '
            j+=1
        result += patience(new_target, new_test)
    
    return result

target = open("target.txt", 'r').read()
test = open("test.txt", 'r').read()

print(patience(target, test))
