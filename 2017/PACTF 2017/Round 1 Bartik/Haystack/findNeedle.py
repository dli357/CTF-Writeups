import json
import base64

file = open('haystack.json', 'r')
data = json.load(file)
#publicKey = data['publicKey']
haystack = data['haystack']
#e = publicKey['publicExponent']
#n = int(publicKey['modulus'])
#sig = haystack[0]['signature']
#sig = base64.b64decode(sig)
#print(sig)
#decSig = int(''.join(str(ord(c)) for c in sig))
#m = pow(decSig, e) % n
#m = str(m)
#md = ''
#for x in range(0, len(m) // 2):
#    md += str(chr(int(m[2*x:2*x+2])))
#print(md)
#print("Sig Ver: " + str(m))
#orData = haystack[0]['data']
#orData = base64.b64decode(orData)
#dataDec = int(''.join(str(ord(c)) for c in orData))
#print("Original Data: " + str(dataDec))
for signature in haystack:
    d = base64.b64decode(signature['data'])
    if d.find('haystack'.encode('utf-8')):
        print(d)
    