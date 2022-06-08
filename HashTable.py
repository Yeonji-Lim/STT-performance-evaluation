class Node:
    def __init__(self, word=None, index=None):
        self.word = word
        self.index = index

class HashTable:
    def __init__(self, n):
        self.n = n
        self.table = [[] for _ in range(n)]

    def mappingTable(self, words):
        for index, word in enumerate(words):
            hash = self.hashValue(word)
            self.add(hash, word, index)

    def hashValue(self, word):
        word_byte = word.encode('utf-8')
        hash = 0
        for i in range(len(word_byte)):
            hash = (word_byte[i]+hash) % self.n
        return hash

    def add(self, key, word, index):
        new_node = Node(word, index)
        self.table[key].append(new_node)

    def len(self):
        return self.n

    def bucketLen(self, key):
        return len(self.table[key])

    def isBucketEmpty(self, key):
        return len(self.table[key]) == 0

    def bucket(self, key):
        return self.table[key]

    def print(self):
        for key, list in enumerate(self.table) :
            if len(list) == 0:
                continue
            print(key, end=" ")
            for node in list:
                print(node.word, node.index, end=" ")
            print()
