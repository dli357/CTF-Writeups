import itertools

data = open('Article.txt', 'r').read()
data = data[2:]
data = data.split("\x00")
newData = []

for x in range(len(data) // 2):
    newData.append(data[2 * x] + data[2 * x + 1])
data = newData

gen = itertools.combinations_with_replacement('abcdefghijklmnopqrstuvwxyz', 6) #1

decrypt = ""
for key in gen:
    print(key)
    decrypt = ""
    for index in range(len(data)):
        char1 = ord(key[index % 6])
        decrypt += chr(int(data[index], 16) ^ char1)
    if "flag" in decrypt:
        print(decrypt)