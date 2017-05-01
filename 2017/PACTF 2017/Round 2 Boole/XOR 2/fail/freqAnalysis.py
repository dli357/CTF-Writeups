import operator

freqOrder = " etaoinshrdlcumwfgypbvkjxqz"

data = open('Article.txt', 'r').read()
data = data[2:]
data = data.split("\x00")
newData = []
for x in range(len(data) // 2):
    newData.append(data[2 * x] + data[2 * x + 1])
data = newData

#every kth letter
k = 12
frequencyMap = {}
for offset in range(k):
    charCount = 0
    map = {}
    charMap = {}
    for index in range(len(data) // k):
        try:
            map[data[k * index + offset]] += 1
        except:
            map[data[k * index + offset]] = 1
        charCount += 1
    sortedMap = sorted(map.items(), key=operator.itemgetter(1))
    sortedMap = sortedMap[::-1]
    print(sortedMap)
    counter = 0
    for character in sortedMap:
        if counter > 25:
            charMap[character[0]] = '-'
        else:
            charMap[character[0]] = freqOrder[counter]
        print(character[0] + ": " + str(character[1]) + ", percentage: " + str(character[1] / charCount))
        counter += 1
    print("Number of unique characters: " + str(len(sortedMap)))
    print("Number of total characters: " + str(charCount))
    frequencyMap[offset] = charMap
#print(frequencyMap)
output = ""
for index in range(len(data)):
    output += frequencyMap[index % k][data[index]]
print(output)
#result = ""
#for char in data:
#    character = int(char, 16)
#    if character == 0:
#        result += " "
#    else:
#        result += char
#print(result)