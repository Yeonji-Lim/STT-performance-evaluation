class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.link = None
class LinkedList:
    def __init__(self):
        self.root = Node()
    def append(self, key, value):
        newNode = Node(key, value)
        curNode = self.root
        cnt = 0
        if curNode.key == None:
            self.root = newNode
        else:
            while curNode.link != None:
                cnt += 1
                curNode = curNode.link
            curNode.link = newNode
        return cnt    
    def delete(self, key):
        curNode = self.root
        if self.root.key == key:
            self.root = self.root.link
        else:
            while curNode.link != None:
                parentNode = curNode
                curNode = curNode.link
                if curNode.key == key:
                    parentNode.link = curNode.link    
    def get(self, key):
        cnt = 0
        curNode = self.root
        while curNode.link != None:
            if curNode.key == key:
                break
            else:
                cnt += 1
                curNode = curNode.link      
        if curNode.key == key:
            return curNode.value, cnt
        else:
            return None     
    def isEmpty(self):
        return self.root.key == None
    def print(self):
        curNode = self.root
        while curNode.link != None:
            print(curNode.key, curNode.value, end=' ')
            curNode = curNode.link
        print(curNode.key, curNode.value)