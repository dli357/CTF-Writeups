import socket
import random
from time import sleep

def generateQuArray():
    bitArr = []
    for x in range(0, 600):
        dict = {}
        dict["basis"] = random.choice("zy")
        dict["value"] = random.choice([-1, 1])
        bitArr.append(dict)
    return bitArr

def recvuntil(s, until, maxlen=2048):
  buf = ''
  while until not in buf and len(buf) < maxlen:
    tmp = s.recv(1).decode('utf-8')
    if len(tmp) == 0:
      raise socket.error
    buf += tmp
  return buf

aBits = []
aCorrectBits = []
aKey = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.connect(('bb8.chal.pwning.xxx', 20811))
recvuntil(s, "(y/N)?")
print("Initiating man-in-the-middle attack...")
for x in range(0, 599):
    #From Alice
    #Measure random y or z from Alice
    #Send Bob your own random qubits
    m = "y\n" + "z\n" + "y\n" + "z\n" + "-1\n" + "n\n"
    s.sendall(m.encode('utf-8'))
    sleep(.1)
    ret = s.recv(400).decode('utf-8')
    ret += s.recv(600).decode('utf-8')
    ret = ret.split("measured ", 2)
    aBits.append(int(ret[1].split("\n")[0]))
    print(x) #I like knowing if my program is running xd

#One qubit offset since Bob starts guessing immediately
m = "y\n" + "z\n" + "y\n" + "z\n" + "-1\n"
s.sendall(m.encode('utf-8'))
sleep(.1)
ret = s.recv(400).decode('utf-8')
ret += s.recv(600).decode('utf-8')
ret = ret.split("measured ", 1)
aBits.append(int(ret[1].split("\n")[0]))
sleep(1)
print("phase 1 complete, onto phase 2")
print(aBits)
print("Bits received from Alice: " + str(len(aBits)))

bobCorrectCounter = 0
for y in range(0, 600):
    #From Bob
    message = "y\n" + "z\n" + "y\n" + "z\n" + "-1\n"
    s.sendall(message.encode('utf-8'))
    sleep(.1)
    ret = s.recv(300).decode('utf-8')
    ret += s.recv(600).decode('utf-8')
    bobGuess = int(ret.split("measured ")[1].split("\n")[0])
    #From Alice
    message = "y\n" + "z\n"
    s.sendall(message.encode('utf-8'))
    sleep(.1)
    ret = s.recv(200).decode('utf-8')
    ret += s.recv(300).decode('utf-8')
    if int(ret.split("measured ")[1].split("\n")[0]) == 1:
        aCorrectBits.append(aBits[y])
    if bobGuess == -1:
        message = "y\n" + "z\n" + "1\n"
        bobCorrectCounter += 1
    else:
        message = "y\n" + "z\n" + "-1\n"
    s.sendall(message.encode('utf-8'))
    print(y) #I like knowing if my program is running xd

print("phase 2 complete, onto phase 3")
print(aCorrectBits)
print("My correct bits: " + str(len(aCorrectBits)))
print("Bob correct bits: " + str(bobCorrectCounter))

if bobCorrectCounter // 2 < 128:
    raise ValueError("Not enough bits to form an encryption key with Bob.")
if len(aCorrectBits) // 2 < 128:
    raise ValueError("Not enough bits to form an encryption key with Alice.")

counter = 0
counterBob = 0
bobLastBitCor = False
counterAlice = 0

while True:
    sleep(.1)
    bobCorrect = False
    m = s.recv(100).decode('utf-8')
    m += s.recv(1024).decode('utf-8')
    print("Premessage: " + m)
    if counter % 2 == 0: #From Bob
        if m.find("classical") == -1:
            message = "y\n" + "z\n"
            s.sendall(message.encode('utf-8'))
            sleep(.1)
            ret = s.recv(300).decode('utf-8')
            ret += s.recv(300).decode('utf-8')
            if int(ret.split("measured ")[1].split("\n")[0]) != -1:
                print("Something went wrong, somebody is eavesdropping on your MITM attack?")
                bobCorrect = False
            else:
                bobCorrect = True
            a = ""
            if counter >= len(aCorrectBits):
                a = "1\n";
            else:
                a = str(aCorrectBits[counter])
            message = "y\n" + "z\n" + a + "\n"
            s.sendall(message.encode('utf-8'))
        else:
            print("Bob's 128-Bit AES Key: " + "0" * 128)
            print(m)
            a = ""
            if counter >= len(aCorrectBits):
                a = "1\n";
            else:
                a = str(aCorrectBits[counter])
            message = "y\n" + "z\n" + a + "\n"
            s.sendall(message.encode('utf-8'))
        counterBob += 1
    else: #From Alice
        if m.find("aborted") != -1:
            print("The connection was aborted by Alice. You sent the wrong qubit?")
            message = ""
            if bobCorrect == True:
                message = "y\n" + "z\n" + "1\n"
            else:
                message = "y\n" + "z\n" + "-1\n"
            s.sendall("1\n".encode('utf-8'))
        elif m.find("classical") == -1:
            message = "y\n" + "z\n" + "y\n" + "z\n"
            s.sendall(message.encode('utf-8'))
            sleep(.1)
            ret = s.recv(300).decode('utf-8')
            ret += s.recv(300).decode('utf-8')
            ret = int(ret.split("measured ")[1].split("\n")[0])
            if ret != 1:
                print("Hm, Alice seemed to have aborted? Something is wrong.")
            s.sendall("1\n".encode('utf-8'))
        else:
            for k in range(0, 128):
                if aCorrectBits[2 * k + 1] == -1:
                    aKey.append('0')
                else:
                    aKey.append('1')
            print("Alice's 128-Bit AES Key: " + str(aKey))
            print(m)
            s.sendall('y\nz\n1\n'.encode('utf-8'))
        counterAlice += 1
    print(counter)
    counter += 1
