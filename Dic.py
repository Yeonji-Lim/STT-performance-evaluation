from LinkedList import LinkedList

class Dic:
    # 해시 테이블의 초기 크기를 지정한다. 일반적으로 item이 가질 수 있는 개수로 지정한다.
    def __init__(self, n):
        self.n = n
        # n개의 Linked List를 가진 List를 정의한다.
        self.table = [LinkedList() for _ in range(n)]
    # 문자열을 숫자로 바꿔주는 함수

    def str2int(self, a):
        val = 0
        for i in range(len(a)):
            val += (i + 1) * ord(a[i])
        return val
    # 해시 테이블에 키와 값 쌍을 입력한다.
    # 키를 숫자로 변환한다음 숫자를 n으로 나눈 나머지 값 위치에 키와 값 쌍을 가진 Node를 삽입한다.

    def add(self, key, value):
        # _tmp = self.str2int(key)
        return self.table[key % self.n].append(key, value)
    # 해시 테이블에서 key를 통해 값을 찾는다.

    def getValue(self, key):
        # key를 숫자로 바꾼 다음 숫자를 n으로 나눈 나머지 값 위치에 있는 Linked List에서 순차 탐색으로 해당 노드 값을 가져온다.
        # 대부분의 경우, Linked List에는 노드가 한개 있는 경우가 많은데 키 충돌이 있다면 1개 이상의 노드가 존재할 것이다.
        _tmp = self.str2int(key)
        return self.table[_tmp % self.n].get(key)

    def delete(self, key):
        _tmp = self.str2int(key)
        self.table[_tmp % self.n].delete(_tmp)

    def print(self):
        for list in self.table :
            if not list.isEmpty():
                list.print()
