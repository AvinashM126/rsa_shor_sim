'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

Project: RSA and Shor's Algorithm
Title: Python implementation of RSA and SHOR
File: rsaModule.py
Incl. modules:  encryptRSA, decryptRSA, generateKeyPairRSA etc...
Author: Avinash M
mail: m.avinash@in.bosch.com
Last Modified Date: 12-11-2024
'''

## Arithmetic imports
from module_scripts.arithmeticModule import \
    moduloInverse_ExtEuclideanAlgorithm, isprime2, generatePrimes,\
    randomSamplePairs, generatePrimePairs, coprimes

def encryptRSA(x, pk):
    enc = [pow(ord(char),pk[0],pk[1]) for char in x]
    return enc

def decryptRSA(y, sk):
    dec = [chr(pow(ch,sk[0],sk[1])) for ch in y]
    return dec

def printRSA_params(p, q, n, phi_n, pk, sk):
    
    print("\n=====================================")
    print('++++----RSA Components----++++')
    print('p=', p, '(',hex(p),')', 'q=', q, '(', hex(q), ')')
    print('n=', n, '(',hex(n),')', 'phi(n)=',phi_n, '(', hex(phi_n), ')')
    print('RSA Key Size: ', n.bit_length(), 'bits')
    print('Public Key:', [hex(pk[0]), hex(pk[1])])
    print('Private Key:', [hex(sk[0]), hex(sk[1])])
    print("=====================================\n")

def generateKeyPairRSA(input_bits):

    # choice = bool(input('\n\nDo you want to generate a list of all primes and sample randomly through the list for the prime pairs (takes longer for larger bit size): (y/n) ==> ') == 'y')
    # if(choice):
    #     primes = generatePrimes(input_bits)
    #     p, q = randomSamplePairs(primes)
    # else:
    #     p, q = generatePrimePairs(input_bits)

    p, q = generatePrimePairs(input_bits)

    ## To recheck prime    
    print('\nPrime Test: ', p, q, '<IS PRIME>' ,[isprime2(p),isprime2(q)])


    ### KEY PAIR GENERATION | RSA

    # p=prime_pair[0]
    # q=prime_pair[1]
    n = p*q
    phi_n = (p-1)*(q-1)

    e = coprimes(phi_n)

    tries = 0
    while(tries<=10):
        tries = tries + 1
        d = moduloInverse_ExtEuclideanAlgorithm(e, phi_n)
        if(d != e):         # Condition to avoid same pk and sk
            break
    if(d == e):
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('The only modulo inverse for e=',e,' is d=',d)
        print('This makes pk and sk same, hence bad key pair...')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('exiting...')
        exit()
    # print('d=',hex(d))

    pk = [e, n]
    sk = [d, n]
    printRSA_params(p, q, n, phi_n, pk, sk)
    return pk, sk