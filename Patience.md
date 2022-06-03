# Hash Chaining Patience Diff

Patience diff 알고리즘에 해시값을 도입하며 많은 부분을 변경한 알고리즘입니다.

patience diff : https://blog.jcoglan.com/2017/09/19/the-patience-diff-algorithm/

## 동작 방식

1. 글의 모든 단어를 나누어 target_words와 test_words에 저장한다.

2. 모든 단어를 해시값으로 바꾸어 해시 테이블에 저장한다. - Hash Seperate Chaining

   이때 해시 값은 한글과 영어에 대해 모두 대응 가능하도록 utf-8 인코딩 값을 활용한다. 

3. target_words에서 해시값이 적게 중복된 단어(unique_word)를 선택한다.

4. test_words에서 unique_words와 해시값이 같은 단어를 찾는다.

5. 해당 단어를 기점으로 앞과 뒤 부분을 나누어 각각 2개의 새로운 target과 test 생성

6. 각각의 (target, test) 쌍에 1-6과정을 반복한다.

7. 남은 부분에 target과 test의 다른 부분이 포함되어있다.

## utf-8 관련 참고 링크

https://studyforus.tistory.com/167

https://infsafe.tistory.com/21



## utf-8 인코딩 값

ㄱㄴㄷ, 가나다, 각난단, 갉낡닭

이 4가지는 모두 길이가 같다. 각 글자는 3byte

## 각 단어의 해시값

알고리즘 강의 target 데이터를 실행해본 결과, 그 값이 3000을 넘어가지 않았다.

띄어쓰기 없이 최대 길이인 15자를 가지는 '클로로트리플루오로에틸렌중합체'의 경우, 8297의 값이 나왔다.

15자인 '힣힣힣힣힣힣힣힣힣힣힣힣힣힣힣'의 경우, 8370의 값이 나왔다.

## 해싱 참고 링크

https://withhamit.tistory.com/401

https://makefortune2.tistory.com/71
