f = open('encrypted.txt', 'r').read()
data = f.strip().split(" ")
flag = ""
for num in data:
    flag += chr((int(num) ^ 46) // 2)
print(flag)