target_file = open("target.txt", 'r')
test_file = open("test.txt", 'r')

# target = target_file.read()
# test = test_file.read()

target_words = target_file.read().split()
test_words = test_file.read().split()

test = '힣힣힣힣힣힣힣힣힣힣힣힣힣힣힣'
test_byte = test.encode('utf-8')

# for i in range(len(test_byte)):
#     print(test_byte[i])

value = 0
for i in range(len(test_byte)) :
    value += test_byte[i]
print(value)


# for word in target_words :
#     print(word)
#     word_byte = word.encode('utf-8')
#     value = 0
#     for i in range(len(word_byte)) :
#         value += word_byte[i]
#     print(value)