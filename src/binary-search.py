if __name__ == '__main__':
  WORDS_PATH = 'scrabble.txt'
  WORDS = []

  with open(WORDS_PATH) as o:
    WORDS = o.readlines()
  left, mid, right = 0, len(WORDS)//2, len(WORDS) - 1
  x = ''
  while(True):
    print()
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    print(WORDS[mid])
    print('is above in [a]fter or [b]efore or did you wi[n]')
    x = input()
    if x == 'n':
      print('grats')
      break
    if x == 'a':
      left = mid
      mid = left + (right - left) // 2
    elif x == 'b':
      right = mid
      mid = right - (mid - left) // 2
    if mid <= left or mid >= right:
      print('is your word', WORDS[mid])
      break