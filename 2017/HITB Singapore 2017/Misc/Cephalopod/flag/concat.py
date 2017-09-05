import os

with open('final.png', 'wb') as final:
    final_bytes = b''
    for num in range(123):
        print(num + 1)
        with open(str(num + 1) + '.bin', 'rb') as f:
            bytes = f.read()
            final_bytes += bytes
    final.write(final_bytes)