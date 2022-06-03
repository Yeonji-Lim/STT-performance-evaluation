import kss
import re

f = open("data/확진자급감_test.txt", 'r')
s = f.read().replace("\n", "")
regex = "\(.*\)|\s-\s.*"
re.sub(regex, '', s)
for sent in kss.split_sentences(s):
    print(sent)

f.close()