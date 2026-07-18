'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

Project: RSA and Shor's Algorithm
Title: Python implementation of RSA and SHOR
File: RSA_SHOR_main.py
Dependencies: shorModule.py, rsaModule.py, arithmeticModule.py
Author: Avinash M
mail: m.avinash@in.bosch.com
Last Modified Date: 12-11-2024
'''

import os
import time
# import numpy as np

from random import randint
from lorem_text import lorem

# Function imports
from module_scripts.arithmeticModule import naive_Factorize
from module_scripts.rsaModule import generateKeyPairRSA, encryptRSA, decryptRSA
from module_scripts.shorModule import shor_algorithm
from module_scripts.shorModule_qpe import WORK_QUBITS

# Shor's quantum algorithm | factor n-bit integers using 2n+2 qubits
available_qubits = 30

def read_file(filename):

    filepath = os.getcwd()+'\\'+filename
    fileOBJ = open(filepath,'r')
    text = fileOBJ.read()
    fileOBJ.close()

    return text

def write_file(filename, text):

    filepath = os.getcwd()+'\\'+filename
    fileOBJ = open(filepath, 'w')
    fileOBJ.write(text)
    fileOBJ.close()

def get_loremtext(words):

    lorem_paragraph = lorem.words(words)
    return lorem_paragraph

def RunModule_keyGen(input_bits):
    rsa_keypairgen_init = time.time()
    pk, sk = generateKeyPairRSA(input_bits)
    rsa_keypairgen_final = time.time()
    print('------------------')
    print('Timing Report: ')
    print('------------------')
    print('Key Generation: ', format("{:>6.4f} s".format(rsa_keypairgen_final-rsa_keypairgen_init)))
    return pk, sk

def RunModule_Enc(resultDispChoice, loremWords, message, pk):
    
    print("\n========================================")
    print('++++----RSA Encryption Components----++++')
    print('Public Key:', [hex(pk[0]), hex(pk[1])])
    print('Message Digest is a LOREM IPSUM TEXT with %3d words, %3d Bytes' %(loremWords, messageBytes))
    print("========================================\n")
    print('-------------------------')
    print('Message: LOREM IPSUM TEXT')
    print('-------------------------')
    if resultDispChoice:
        print(message)
    else:
        print('<Text Too Large to Print>')
    ### ENCRYPTION

    rsa_enc_init = time.time_ns()
    encMsg = encryptRSA(message, pk)
    rsa_enc_final = time.time_ns()
    
    encString = ''.join(map(lambda x: str(format(x, '0{}x'.format(4))), encMsg))
    print('\n------------------')
    print('Cipher Text: ')
    print('------------------')
    if resultDispChoice:
        print(encString)
    else:
        print('<Text Too Large to Print>')

    print('\n------------------')
    print('Timing Report: ')
    print('------------------')
    print('Encryption: ', format("{:>6.4f} ns".format(rsa_enc_final-rsa_enc_init)))
    return encMsg, encString


def RunModule_Dec(resultDispChoice, loremWords, encString, encMsg, sk):
    ### DECRYPTION

    rsa_dec_init = time.time_ns()
    decMsg = decryptRSA(encMsg, sk)
    rsa_dec_final = time.time_ns()

    decString = ''.join(decMsg)
    cipherBytes = encString.__sizeof__() - [].__sizeof__() - 1

    print("\n========================================")
    print('++++----RSA Decryption Components----++++')
    print('Private Key:', [hex(sk[0]), hex(sk[1])])
    print('Cipher Digest is %3d Bytes' %(cipherBytes))
    print("========================================\n")
    
    print('------------------')
    print('Cipher Text: ')
    print('------------------')
    if resultDispChoice:
        print(encString)
    else:
        print('<Text Too Large to Print>')

    print('\n------------------')
    print('Decrypted Message:')
    print('------------------')
    if resultDispChoice:
        print(decString)
    else:
        print('<Text Too Large to Print>')
        

    print('\n------------------')
    print('Timing Report: ')
    print('------------------')
    print('Decryption: ', format("{:>6.4f} ns".format(rsa_dec_final-rsa_dec_init)))
    return decString

if __name__ == '__main__':

    '''
    
    ### To test GCD and modulo inverse which is based on Extended Euclidean Algorithm

    (a, b) = input('Enter the Input: (a,b): ').split(',')
    bezout_coeff, gcd_out = gcd_extEucideanAlgorithm(int(a), int(b))
    print('Bezout coefficients are: ', bezout_coeff)
    print('GCD(',a,',', b, ') = ', gcd_out)

    (num, modulo) = input('Enter the number and modulo to find the inverse: (x, n) -> ').split(',')
    num, modulo = int(num), int(modulo)
    modinv_EEA_init = time.time() * 1000
    mod_inv = moduloInverse_ExtEuclideanAlgorithm(num, modulo)
    modinv_EEA_final = time.time() * 1000
    print('The modulo inverse is: ', mod_inv, modinv_EEA_final-modinv_EEA_init, 'sec')
    print('Verification: (x*mod_inv) = 1 (modulo n)',(num*mod_inv%modulo)==1)
    
    '''
    ### RSA and SHOR's Algorithm
    
    os.system('cls')
    # os.system('python -V')
    choice_shor = bool(input('Is the RSA to test SHOR\'s Algorithm (y/n): ') == 'y')
    # choice_shor = True
    ## Message input
    # loremWords = int(input('Enter the word count to generate the message to be encrypted: '))
    loremWords = 20
    message = lorem.words(loremWords)
    txtAscii = [ord(char) for char in message]
    txtArray = ','.join(map(lambda message: str(message), txtAscii))
    messageBytes = message.__sizeof__() - [].__sizeof__() - 1

    if(choice_shor):
        print('To implement SHOR\'s Algorithm, IBMQX backend simulator provides 30 qubits.')
        print('Shor\'s quantum algorithm currently factors n-bit integers using 2n+2 qubits')
        print("Input Bits: bit-length used to generate each prime p and q.")
        input_bits = int(input('Enter input bits for KeyGeneration | (max 14): '))
        if(input_bits >= available_qubits):
            print('Cannot implement SHOR\'s due to large N.')
            exit()
    else:
        print("Input Bits: bit-length used to generate each prime p and q.")
        input_bits = int(input('Enter input bits for KeyGeneration: '))
        


# Key Generation
    pk, sk = RunModule_keyGen(input_bits)
    
    resultDispChoice = True
    if loremWords > 50:
        resultDispChoice = False    

    os.system('pause')

# Encrypt the message
    encMsg, encString = RunModule_Enc(
        resultDispChoice=resultDispChoice, 
        loremWords=loremWords, 
        message=message, 
        pk=pk
        )

# Choice to run naive factorization algorithm to get the private key (Brute Force)
    print('\n\nBRUTE FORCE - Randomized Naive Factorization Algorithm')
    naivefact_Choice = bool(input('\nDo you want to run naive factorization algorithm. (y/n): ') == 'y')
    if(naivefact_Choice):
        print('\nRunning Naive Prime Factorization Randomized Algorithm:')
        naive_fact_init = time.time()
        n_p, n_q = naive_Factorize(pk[1], input_bits)
        naive_fact_final = time.time()
        print("The Primes are p=",hex(n_p), 'q=',hex((int(n_q))))
        print("Processing Time: ", format("{:>6.4f} s".format(naive_fact_final-naive_fact_init)))
        os.system('pause')

# SHOR's Algorithm to factor the modulus and get the private key
    if(choice_shor):
        # CHOICE: Select which Shor's implementation to use
        print('\n' + '='*70)
        print('SHOR\'S ALGORITHM - Implementation Selection')
        print('='*70)
        print('\nAvailable Implementations:')
        print('\n1) flat/classical - Classical-Hybrid (Original)')
        print('\n2) qpe - Quantum Phase Estimation (Improved)')
        print('\n3) auto - Run BOTH and compare')
        
        shor_choice = input('\nSelect method (1/2/3) [default=3]: ').strip() or '3'
        
        method_map = {'1': 'flat', '2': 'qpe', '3': 'auto'}
        method = method_map.get(shor_choice, 'auto')

        rsa_bits = pk[1].bit_length()
        qpe_supported = rsa_bits <= WORK_QUBITS

        if method == 'qpe' and not qpe_supported:
            print(
                f"\nQPE requires RSA modulus bits <= {WORK_QUBITS}. "
                f"Your modulus uses {rsa_bits} bits, so the selection falls back to flat/classical."
            )
            method = 'flat'
        elif method == 'auto' and not qpe_supported:
            print(
                f"\nAuto mode will skip QPE because RSA modulus uses {rsa_bits} bits "
                f"and QPE work register supports only {WORK_QUBITS} bits."
            )
        
        SHOR_breaker_init = time.time()
        sk_shor = shor_algorithm(pk, method=method)
        SHOR_breaker_final = time.time()
        
        print('\n------------------')
        print('Overall Timing Report: ')
        print('------------------')
        print("Total Shor's execution time: ", format("{:>6.4f} s\n".format(SHOR_breaker_final-SHOR_breaker_init)))
        
        sk_decoding = sk_shor
        print('The Private Key generated by SHOR\'s Algorithm is: ', [hex(sk_decoding[0]), hex(sk_decoding[1])])
    else:
        sk_decoding = sk

# Decrypt the message
    decMsg = RunModule_Dec(
        resultDispChoice=resultDispChoice, 
        loremWords=loremWords, 
        encString=encString, 
        encMsg=encMsg, 
        sk=sk_decoding
        )
    print('\nThe original message is same as the decrypted message: ', message == decMsg, end='\n')