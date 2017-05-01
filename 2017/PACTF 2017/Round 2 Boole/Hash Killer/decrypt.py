import Crypto.Cipher.AES
import Crypto.Util.number
import base64

key = "76b7593457e2ab50befe2dcd63cf388f".encode('utf-8')
c = "mJRKaaMSR1atUGs0kOkAJP3dty9tjCvXKMzWDHtZdRQ="
c = base64.b64decode(c)
print(c)
#key = bytes.fromhex(key)
cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_ECB)
message = cipher.decrypt(c)
print(message)