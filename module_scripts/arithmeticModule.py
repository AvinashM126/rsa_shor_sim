'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

Project: RSA and Shor's Algorithm
Title: Python implementation of RSA and SHOR
File: arithmeticModule.py
Incl. modules: isprime, isprime2, countingBits, coprimes, generatePrimes, moduloInverse_Naive, gcd_extEucideanAlgorithm, moduloInverse_ExtEuclideanAlgorithm
Author: Avinash M
mail: m.avinash@in.bosch.com
Last Modified Date: 12-11-2024
'''

# PREAMBLES
from math import sqrt
from random import sample, getrandbits, randint

def isprime(num):
    if(num == 0 or num == 1): 
        return False
    elif(num//2 <= 2 and num!=4):
        return True
    elif(num == 4):
        return False
    else:
        for i in range(2, num//2):
            if (num%i==0): 
                return False
    return True

## Provided by the QUANTUM CRACKING ENCRYPTION git repo code, in RSA_module.py file
def isprime2(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, int(sqrt(num)) + 1):
            if num % i == 0:
                return False
    return True

def countingBits(num):
    ref_num=1
    bit_count = -1
    while(ref_num <= num):
        ref_num <<= 1
        bit_count+=1
    return bit_count

def generatePrimes(input_bits):

    '''
    Prime Number Generation in the given Range

    Range -> [0,N]

    '''
    num = 2**input_bits
    primes=[]
    for i in range(num):
        if(isprime2(i)):
            primes.append(i)
    print('Total no. of primes in the range [ 0 ,',num,'] = ',len(primes))
    return primes

def randomSamplePairs(primes):
    return sample(primes,2)

def generatePrimeNumber(input_bits):
    prime = getrandbits(input_bits)
    
    while(not isprime2(prime)):
        prime = (1<<input_bits) - getrandbits(input_bits)
    return prime

def generatePrimePairs(input_bits):
    prime_pair = [0,0]
    for i in range(len(prime_pair)):
        while(not isprime2(prime_pair[i])):
            prime_pair[i]=(1<<input_bits) - getrandbits(input_bits)
    return prime_pair

def coprimes(num):
    while(True):
        num_coprime = randint(1, num-1)
        _, g = gcd_extEucideanAlgorithm(num_coprime, num)
        if(g==1):
            return num_coprime

def moduloInverse_Naive(num, modulo):
    for i in range(modulo):
        if((num*i)%modulo==1):
            return i

def gcd_extEucideanAlgorithm(a, b):
    
    # Algorithm: Extended Euclidean Algorithm
    # Bezout identity ==> a*s0 + b*t0 = gcd(a,b)
    # input: a,b
    # outputs: Bezout coeffs=(s0, t0), gcd

    # initial values
    (r0, r1) = (a,b)
    (s0, s1) = (1,0)
    (t0, t1) = (0,1)

    # iteration
    while(r1 != 0):
        q = r0 // r1
        (r0, r1) = (r1, r0 - q * r1)
        (s0, s1) = (s1, s0 - q * s1)
        #(t0, t1) = (t1, t0 - q * t1)
        #print((r0,r1), (s0,s1), (t0,t1))
    
    if(b != 0):
        t0 = (r0 - s0 * a)//b
    else:
        t0 = 0
    
    return list((s0, t0)),(r0)


def moduloInverse_ExtEuclideanAlgorithm(num, modulo):
    bezout_coeff, gcd_out = gcd_extEucideanAlgorithm(modulo, num)
    if(gcd_out > 1):
        print(num,'is not invertible')
    if(bezout_coeff[1] < 0):
        bezout_coeff[1] += modulo
    
    return bezout_coeff[1]

def naive_Factorize(num, numBits):
    num_UL = sqrt(num)
    r = 1
    primeFactorNaive = 0
    while(r != 0 and r != num):
        primeFactorNaive = generatePrimeNumber(numBits)
        r = num % primeFactorNaive
    return primeFactorNaive, num/primeFactorNaive