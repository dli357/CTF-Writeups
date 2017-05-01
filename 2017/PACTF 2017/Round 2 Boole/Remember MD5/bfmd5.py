import hashlib
from time import sleep

md5 = "1b657b7fe26eda5b3c1309d340f1674d"

def ternary (n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

digit = 0
counter = 0
guessCounter = 0
guessB3 = 0
guess = "aaaaaaaaaaaaaaa"
while True:
    result = hashlib.md5(guess.encode('utf-8')).hexdigest()
    print(guess)
    if result == md5:
        print("Hash Found:")
        print(guess)
        sleep(10)
        break
    else:
        guessCounter += 1
        guessB3 = str(ternary(guessCounter).zfill(15))
        newGuess = ""
        for char in guessB3:
            if char == '0':
                newGuess += 'a'
            elif char == '1':
                newGuess += 'b'
            elif char == '2':
                newGuess += 'c'
        guess = newGuess