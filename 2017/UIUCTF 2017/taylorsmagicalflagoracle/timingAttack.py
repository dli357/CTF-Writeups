import socket
import time
import itertools

def recvuntil(s, until, maxlen=2048):
  buf = ''
  while until not in buf and len(buf) < maxlen:
    tmp = s.recv(1).decode('utf-8')
    if len(tmp) == 0:
        print(buf)
        raise socket.error
    buf += tmp
  return buf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('challenge.uiuc.tf', 11340))

print("Welcome to:")
print("DENNIS'S MAGICAL TAYLOR'S MAGICAL FLAG ORACLE CRACKER!")

#print(recvuntil(s, "'").decode('utf-8'))


flag = "flag{trchrus"
response = "> No"
charset = "}abcdefghijklmnopqrstuvwxyz1234567890_"
while "No" in response:
    largestTime = 0
    likelyChar = ""
    for x in range(len(charset)):
        print(flag + charset[x])
        m = flag + charset[x] + "\n"
        s.send(m.encode('utf-8'))
        pre = time.clock()
        response = s.recv(2048).decode('utf-8')
        timeTaken = time.clock() - pre
        print(timeTaken)
        print(timeTaken - largestTime)
        if timeTaken > largestTime:
            if largestTime != 0 and timeTaken - largestTime > .20:
                largestTime = timeTaken
                likelyChar = charset[x]
                break
            elif timeTaken - largestTime < -0.2:
                break
            else:
                largestTime = timeTaken
                likelyChar = charset[x]
    flag += likelyChar
print(response)