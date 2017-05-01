data = open('daString.txt', 'r').read()
final = ''
print(data)
for char in data:
    final += chr(ord(char) ^ 97)
final = final.strip(",")
print(final)
final = final.split(",")
flag = ""
prev = 0
for c in range(len(final)):
    index = 24 - c
    char = chr(int(final[index]) - prev)
    flag += char
    prev = ord(char)
flag = flag[::-1]
print(flag)