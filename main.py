import kss
import re

def clean_text(inputString):
  text_rmv = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', inputString)
  return text_rmv

f = open("data/부럽지가않어_target.txt", 'r')
# s = clean_text(f.read().replace("\n", ""))
s = f.read()
for sent in kss.split_sentences(s):
    print(sent)

f.close()