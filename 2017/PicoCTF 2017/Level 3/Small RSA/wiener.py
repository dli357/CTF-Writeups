from sympy import *
import re
import sys
import codecs
import binascii

#Use Wiener's attack since we can infer that d is small
#Must have text files named e.txt, n.txt, and c.txt (if no c, just leave it blank)

#Find the continued fractions expansion of numerator n
#and denominator d
def cf_expansion(n, d):
    e = []

    q = n // d
    r = n % d
    e.append(q)

    while r != 0:
        n, d = d, r
        q = n // d
        r = n % d
        e.append(q)

    return e
    
#Find the convergence of a continued fraction expansion e

def convergents(e):
    n = [] # Nominators
    d = [] # Denominators

    for i in range(len(e)):
        if i == 0:
            ni = e[i]
            di = 1
        elif i == 1:
            ni = e[i]*e[i-1] + 1
            di = e[i]
        else: # i > 1
            ni = e[i]*n[i-1] + n[i-2]
            di = e[i]*d[i-1] + d[i-2]

        n.append(ni)
        d.append(di)
        yield (ni, di)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

        
with open('c.txt', 'r') as c:
    with open('n.txt', 'r') as n:
        with open('e.txt', 'r') as e:
            c = int(c.read())
            n = int(n.read())
            e = int(e.read())
            expansion = cf_expansion(e, n)
            convergence = convergents(expansion)
            p = 0;
            q = 0;
            phi = 0;
            for di, ki in convergence:
                print("Di: " + str(di) + " Ki: " + str(ki))
                if di == 0:
                    continue;
                guess = (e * ki - 1) // di
                p = Symbol('p', integer=True)
                roots = solve(p**2 + (guess - n - 1)*p + n, p)
                if (len(roots) == 2):
                    pp, pq = roots
                    if (pp * pq == n):
                        print("Possible Phi: " + str(guess))
                        print("P: " + str(pp))
                        print("Q: " + str(pq))
                        p = pp;
                        q = pq;
                        break;
            
            d = modinv(e, (p - 1) * (q - 1))
            print(d)
            message = (c ^ int(d)) % n
            print("M:" + str(message))
            message = codecs.decode(hex(message)[2:-1], 'hex')
            print(message)