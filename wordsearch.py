import sys
import time
import os

if len(sys.argv) is not 3:
  print(f"Usage: {sys.argv[0]} <wordlist filename> <character set>")
  sys.exit(1)

filepath = sys.argv[1]
characters = sys.argv[2]

def word_in_set(word, charset):
  remaining_set = charset
  for letter in word:
    pos = remaining_set.find(letter)
    if pos == -1:
      pos = remaining_set.find(".")
      if pos == -1:
        return False
      else:
        remaining_set = remaining_set[:pos] + remaining_set[pos+1:]
    else:
      remaining_set = remaining_set[:pos] + remaining_set[pos+1:]
  return True

goodwords = []
begin = time.time()
readfile = open(filepath,"r")
for word in readfile:
  word = word[:-1]
  if word_in_set(word, characters):
    goodwords.append(word)
end = time.time()
print(f"{len(characters)} characters filtered in {end - begin} seconds")

begin = time.time()
goodwords.sort(key=len)
goodwords.reverse()
end = time.time()
print(f"{len(goodwords)} good words sorted in %f seconds")

for word in goodwords:
  print(word)
