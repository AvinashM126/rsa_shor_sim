'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

Project: RSA and Shor's Algorithm
Title: Python implementation of RSA and SHOR
File: shorModule.py
Incl. modules: period, shors_breaker, shor_algorithm
Author: Avinash M
mail: m.avinash@in.bosch.com
Last Modified Date: 12-11-2024

Shor's Algorithm Source Credits: Jordi Garcia Castillon, Quantum Cracking Encryption, GitHub Project
Git Repo: https://github.com/gcjordi/quantum_cracking_encryption
'''
import numpy as np
from random import randint
# QISKIT PREAMBLES
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.providers.basic_provider import BasicProvider
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile

from module_scripts.arithmeticModule import \
    gcd_extEucideanAlgorithm, moduloInverse_ExtEuclideanAlgorithm
from module_scripts.rsaModule import printRSA_params

# Shor's quantum algorithm | factor n-bit integers using 2n+2 qubits
available_qubits = 30

def period(backend, a: int, N: int) -> int:

    '''
    This function implements the period finding subroutine of Shor's algorithm using a quantum circuit.
    It takes as input a quantum backend, an integer 'a', and an integer 'N
    representing the number to be factored. The function returns the period 'r' of the function f(x) = a^x mod N.
    The function initializes a quantum circuit with 'available_qubits' qubits and classical bits.
    Args:
        backend: A quantum backend from Qiskit Aer.
        a (int): An integer 'a' used in the function f(x) = a^x mod N.
        N (int): The integer 'N' to be factored.
    Returns:
        r (int): The period of the function f(x) = a^x mod N
    '''

    r: int = -1
    qr = QuantumRegister(available_qubits)   
    cr = ClassicalRegister(available_qubits)
    qc = QuantumCircuit(qr,cr)
    x0 = randint(1, N-1) 
    x_binary = np.zeros(available_qubits, dtype=bool)
    
    for i in range(1, available_qubits + 1):
        bit_state = (N%(2**i)!=0)
        if bit_state:
            N -= 2**(i-1)
        x_binary[available_qubits-i] = bit_state    
    
    for i in range(0,available_qubits):
        if x_binary[available_qubits-i-1]:
            qc.x(qr[i])
    x = x0
    
    while np.logical_or(x != x0, r <= 0):
        r+=1
        qc.measure(qr, cr) 
        for i in range(0,3): 
            qc.x(qr[i])
        qc.cx(qr[2],qr[1])
        qc.cx(qr[1],qr[2])
        qc.cx(qr[2],qr[1])
        qc.cx(qr[1],qr[0])
        qc.cx(qr[0],qr[1])
        qc.cx(qr[1],qr[0])
        qc.cx(qr[3],qr[0])
        qc.cx(qr[0],qr[1])
        qc.cx(qr[1],qr[0])
        
        new_ckt = transpile(qc, backend = backend)

        job = backend.run(new_ckt)

        result = job.result()

        counts = result.get_counts()
        
        # print(counts)
        # print(qc)
        # qc.draw(fold=-1)  # -1 means 'do not fold'
        
        results = [[],[]]
        for key,value in counts.items(): 
            results[0].append(key)
            results[1].append(int(value))
        s = results[0][np.argmax(np.array(results[1]))]
    return r

def shors_breaker(backend, N):
    N = int(N)
    while True:
        a=randint(0,N-1)
        _, g=gcd_extEucideanAlgorithm(a,N)
        if g!=1 or N==1:
            return g,N//g
        else:
            r=period(backend,a,N) 
            if r % 2 != 0:
                continue
            elif pow(a,r//2,N)==-1:
                continue
            else:
                _, p=gcd_extEucideanAlgorithm(pow(a,r//2)+1,N)
                _, q=gcd_extEucideanAlgorithm(pow(a,r//2)-1,N)
                if p==N or q==N:
                    continue
                return p,q

def shor_algorithm(pk):

    print('===============================')
    print('\nShor\'s Algorithm:\n')
    print('===============================')
    
    ### Assertions
    n = pk[1]
    assert n > 0,"Input must be positive"
    assert n < 2**available_qubits, (str(n)+' is too big for'+backend.name)

    # AER Backend Selection
    print('-----------------------------------')
    print('Available Backends and qubits')
    print('-----------------------------------')
    
    # Backend selection
    print('\n[Backend Selection]')
    print('-' * 70)
    backends_list = []
    for backend in Aer.backends():
        qubits = backend.configuration().num_qubits
        backends_list.append((backend.name, qubits))
        print(f"  • {backend.name:25} ({qubits:2} qubits)")
    
    backend = Aer.get_backend('qasm_simulator')
    print(f'\nSelected: {backend.name} ({backend.configuration().num_qubits} qubits)')

    p_shor,q_shor = shors_breaker(backend, n)

    phi_n = (p_shor-1) * (q_shor-1)  

    e = pk[0]

    # print('e from pk = ', e_shor)
    while(True):
        d_shor = moduloInverse_ExtEuclideanAlgorithm(e, phi_n)
        if(d_shor != e):         # Condition to avoid same pk and sk
            break
    
    pk_shor = pk
    sk_shor = [d_shor, n]
    printRSA_params(p_shor, q_shor, n, phi_n, pk_shor, sk_shor)
    return sk_shor