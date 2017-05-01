from PIL import Image

fileName = 'test.png'
im = Image.open(fileName)
px = im.load()
width = im.width
height = im.height
charStr = ''
for y in range(0, height):
    for x in range(0, width):
        for color in range(0, 3):
            num = px[x, y][color]
            charStr += str(chr(num // 2))
print(charStr)