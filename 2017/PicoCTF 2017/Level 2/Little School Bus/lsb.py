from bitstring import BitArray

fileName = 'littleschoolbus.bmp'
searchString = 'flag'

bytes = open('littleschoolbus.bmp', 'rb').read()
bytes = bytearray(bytes)
binary = str(bin(int.from_bytes(bytes, 'big', signed=False)))
hexSearch = ''
for x in range(0, len(searchString)):
    hexSearch += format(ord(searchString[x]), '#04x')[2:]
print('Hex string to search: ' + hexSearch)

for offsetX in range(0, 7):
    for offsetY in range(0, 7):
        lsbChar = ''
        binFinal = ''
        binary = binary[offsetX:len(binary) - 1]
        while ((len(binary)) % 8 != 0):
            binary += '0'
        for b in range(0, int(len(binary) / 8)):
            binFinal += binary[b * 8 + 7]
        lsb = binFinal[offsetY:len(binFinal) - 1]
        while ((len(lsb)) % 8 != 0):
            lsb += '0'
        for a in  range(0, int(len(lsb) / 8)):
            hex = int(lsb[a * 8:(a + 1) * 8], 2)
            lsbChar += format(hex, '#04x')[2:]
        if (lsbChar.count(hexSearch) > 0):
            start = lsbChar.find(hexSearch)
            end = lsbChar.rfind(hexSearch)
            output = ''
            for c in range(0, end - start + 100): #print 100 bytes following search
                output += chr(int(lsbChar[c*2+start:c*2+2+start], 16))
            print('String Found: ' + output)
            print('X offset: ' + str(offsetX) + ', Y offset: ' + str(offsetY))