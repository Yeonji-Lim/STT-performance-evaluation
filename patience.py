from HashTable import HashTable

target_file = open("target.txt", 'r')
test_file = open("test.txt", 'r')

# target_words = target_file.read().split()
# test_words = test_file.read().split()

target_words = "john is holly".split()
test_words = "holly jeongje john".split()

table_size = 997
target_table = HashTable(table_size)
test_table = HashTable(table_size)

target_table.mappingTable(target_words)
test_table.mappingTable(test_words)

target_arr = []
for i in range(target_table.len()):
    if not target_table.isBucketEmpty(i) and not test_table.isBucketEmpty(i):
        target_arr.append((i, target_table.bucketLen(i)))  # (해시값, 버킷의 원소수)

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
        elif test_table.bucketLen(low_arr[l][0]) < test_table.bucketLen(high_arr[h][0]):
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

result_words = ["" for _ in range(len(target_words))]
visited_target = [False for _ in range(len(target_words))]
visited_test = [False for _ in range(len(test_words))]

def isAllEqual(bucket):
    firstWord = bucket[0].word
    for node in bucket:
        if node.word != firstWord:
            return False
    return True

for hash, num in target_arr:

    # TODO 앞에서 유니크 단어 뽑았던거 기억해두었다가 지금 target과 test의 인덱스가 구간이 안맞으면 pass

    target_bucket = target_table.bucket(hash)
    test_bucket = test_table.bucket(hash)
    if len(target_bucket) == len(test_bucket) and \
        target_bucket[0].word == test_bucket[0].word:

        if isAllEqual(target_bucket) and isAllEqual(test_bucket): 
            for node in target_bucket:
                visited_target[node.index] = True
                result_words[node.index] = node.word
            for node in test_bucket:
                visited_test[node.index] = True
            continue
           
        # 142 우리 112 따라 140
        # 688 정렬이 51 정렬이 148 정렬이 165
        # 688 정렬이 46 정렬이 137 정맥이 153
        for i, node in enumerate(target_bucket) :
            if node.word != test_bucket[i].word:
                break
            result_words[node.index] = node.word
            visited_target[node.index] = True
            visited_test[test_bucket[i].index] = True

print()
print(" ".join(result_words))
