import codecs
enc_hex = open('Article.txt', 'r').read()
enc_hex = enc_hex[2:].strip("\x00").split("\x00")

newData = []
enc_ascii = ""

for x in range(len(enc_hex) // 2):
    newData.append(int(enc_hex[2 * x] + enc_hex[2 * x + 1], 16))
    enc_ascii += chr(int(enc_hex[2 * x] + enc_hex[2 * x + 1], 16))

enc_numbers = newData
