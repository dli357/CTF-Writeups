import socket
import math

def primes_sieve2(limit):
    a = [True] * limit                          # Initialize the primality list
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):     # Mark factors non-prime
                a[n] = False

limit = 2000
print(limit)
primes = primes_sieve2(limit)
primesList = []
for num in primes:
    primesList.append(num)
    
flagFound = False
while flagFound == False:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('shell2017.picoctf.com', 25893))
    s.recv(1024)
    ne = s.recv(1024)
    ne = str(ne).split(" ")
    n = ne[1]
    n = int(n[:-4])
    e = ne[2]
    e = int(e[:-7])
    sigs = {}
    for prime in primesList:
        m = str(prime) + "\n"
        s.send(m.encode('utf-8'))
        s.recv(1024)
        sig = s.recv(1024).decode('utf-8')
        sig = sig.strip(" ")
        sig = sig.split("Enter")[0]
        sig = int(sig)
        sigs[prime] = sig
    s.send("-1\n".encode('utf-8'));
    s.recv(1024)
    challenge = s.recv(1024).decode('utf-8').strip(" ").split("Enter")[0]
    print("Challenge: " + challenge)
    challenge = int(challenge)
    forgery = 1
    factorization = []
    for prime in primesList:
        while (challenge % prime) == 0:
            forgery = (forgery * sigs[prime]) % n
            challenge = challenge // prime
            factorization.append(prime)
    print("Prime Factorization: " + str(factorization))
    print("Forgery: " + str(forgery))
    forgery = str(forgery) + "\n"
    s.send(forgery.encode('utf-8'))
    output = s.recv(1024).decode('utf-8')
    if output != "Nope, that's wrong!":
        flagFound = True
        print(output)
        print(s.recv(1024).decode('utf-8'))
    else:
        print("Flag not found, retrying...")