import Crypto.Cipher.AES
import Crypto.Util.number

aKey = ['0', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '1', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '1', '0', '1', '1', '0', '1', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '0', '1', '1', '0', '1', '0', '1', '1', '1', '0', '0', '1', '1', '0', '0', '0']
bKey = '0' * 32
aC = "409e14dd0b54d4cac3f6befac21c73f4a77953f4b932cb9500ed2698101803b2"
bC = "ba05c06848288e173a8b34c03dc72fd6b531f386efdc6cd065c3ee6baf3fcbf55f10e1e69db386cf0c168d91078c4dbd"
aC = bytes.fromhex(aC)
bC = bytes.fromhex(bC)
aKey = "".join(['1' if c == '1' else '0' for c in aKey])
bKey = "".join(['1' if c == '1' else '0' for c in bKey])
aKey = hex(int(aKey, 2))[2:]
aKey = bytes.fromhex(aKey)
bKey = bytes.fromhex(bKey)
print(aKey)
print(bKey)
cipherB = Crypto.Cipher.AES.new(bKey, Crypto.Cipher.AES.MODE_ECB)
cipherA = Crypto.Cipher.AES.new(aKey, Crypto.Cipher.AES.MODE_ECB)
message1 = cipherA.decrypt(aC)
message2 = cipherB.decrypt(bC)
print((message1.strip() + message2.strip()).decode('utf-8'))
