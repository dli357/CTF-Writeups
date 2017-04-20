from PIL import Image

im = Image.open('littleschoolbus.bmp')
px = im.load()
width = im.width
height = im.height
lsb = ''
for y in range(0, height):
    for x in range(0, width):
        for color in range(0, 3):
            binary = bin(px[x, y][color])
            lsb += str((binary)[len(binary) - 1])
lsbChar = ''
lsb = lsb[8:len(lsb) - 1]
while ((len(lsb)) % 8 != 0):
    lsb += '0'
for a in  range(0, int(len(lsb) / 8)):
    lsbChar += chr(int(lsb[a * 8:(a + 1) * 8], 2))
print(lsbChar)