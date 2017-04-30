import hashlib
import rsa
import binascii
import os
from gmpy2 import mpz, iroot, powmod, mul, t_mod

def to_bytes(n):
    """ Return a bytes representation of a int """
    return n.to_bytes((n.bit_length() // 8) + 1, byteorder='big')

def from_bytes(b):
    """ Makes a int from a bytestring """
    return int.from_bytes(b, byteorder='big')

def get_bit(n, b):
    """ Returns the b-th rightmost bit of n """
    return ((1 << b) & n) >> b

def set_bit(n, b, x):
    """ Returns n with the b-th rightmost bit set to x """
    if x == 0: return ~(1 << b) & n
    if x == 1: return (1 << b) | n

def cube_root(n):
    return int(iroot(mpz(n), 3)[0])
    
message = "right below".encode("ASCII")
message_hash = hashlib.sha256(message).digest()

ASN1_blob = rsa.pkcs1.HASH_ASN1['SHA-256']

suffix = b'\x00' + ASN1_blob + message_hash

#binascii.hexlify(suffix)

#suffix[-1]&0x01 == 1

sig_suffix = 1

for b in range(len(suffix)*8):
    if get_bit(sig_suffix ** 3, b) != get_bit(from_bytes(suffix), b):
        sig_suffix = set_bit(sig_suffix, b, 1)

#to_bytes(sig_suffix ** 3).endswith(suffix)


#len(to_bytes(sig_suffix ** 3)) * 8

while True:
    prefix = b'\x00\x01' + os.urandom(2048//8 - 2)
    sig_prefix = to_bytes(cube_root(from_bytes(prefix)))[:-len(suffix)] + b'\x00' * len(suffix)
    sig = sig_prefix[:-len(suffix)] + to_bytes(sig_suffix)
    if b'\x00' not in to_bytes(from_bytes(sig) ** 3)[:-len(suffix)]: break

print(binascii.hexlify(sig))