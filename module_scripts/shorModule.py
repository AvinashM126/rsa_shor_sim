'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

Project: RSA and Shor's Algorithm
Title: Shor's Algorithm Router/Dispatcher
File: shorModule.py
Author: Avinash M
Last Modified Date: 2026-01-16

DESCRIPTION:
Router module that provides dynamic selection between isolated implementations:
- shorModule_flat.py: Classical-hybrid (original, brute-force period finding)
- shorModule_qpe.py: Quantum Phase Estimation (proper two-register QPE)

ARCHITECTURE PRINCIPLE:
This module ONLY contains routing logic. NO implementation code lives here.
- All period finding logic is in isolated modules
- All factoring logic is in isolated modules
- This router simply dispatches based on the 'method' parameter
Isolation is CRITICAL for maintainability and clarity.
'''

import time
from module_scripts import shorModule_flat
from module_scripts import shorModule_qpe


def shor_algorithm(pk, method='auto'):
    '''
    Unified Shor's algorithm interface with dynamic method selection.
    
    Routes to appropriate isolated implementation based on method parameter.
    
    Args:
        pk: Public key (e, N)
        method: Implementation to use
                - 'flat' or 'classical': Use classical-hybrid (shorModule_flat)
                - 'qpe': Use quantum phase estimation (shorModule_qpe)
                - 'auto': Try both, show comparison
    
    Returns:
        sk: Secret key (d, N)
    '''
    
    if method == 'auto':
        return _compare_implementations(pk)
    elif method in ['flat', 'classical']:
        return shorModule_flat.shor_algorithm(pk)
    elif method == 'qpe':
        return shorModule_qpe.shor_algorithm(pk)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'flat', 'qpe', or 'auto'")


def _compare_implementations(pk):
    '''
    Run both implementations and compare results.
    
    Args:
        pk: Public key
    
    Returns:
        sk: Best result (prefers classical if both succeed)
    '''
    
    print('\n' + '=' * 80)
    print("COMPARISON: Both Shor's Algorithm Implementations")
    print('=' * 80)
    
    N = pk[1]
    e = pk[0]
    
    # Classical implementation
    print('\n' + '*' * 80)
    print('1 CLASSICAL-HYBRID (shorModule_flat.py)')
    print('*' * 80)
    print('   Architecture: Single flat 30-qubit register')
    print('   Period Finding: Classical iteration loop + CNOT swaps')
    print('   Status: RUNNING...\n')
    
    time1_start = time.time()
    try:
        sk_flat = shorModule_flat.shor_algorithm(pk)
        time1_end = time.time()
        time1_elapsed = time1_end - time1_start
        
        if sk_flat and sk_flat[0] > 0:
            print(f'\n SUCCESS in {time1_elapsed:.2f}s')
            d_flat = sk_flat[0]
        else:
            print(f'\n FAILED in {time1_elapsed:.2f}s')
            d_flat = None
    except Exception as e:
        time1_end = time.time()
        time1_elapsed = time1_end - time1_start
        print(f'\n ERROR in {time1_elapsed:.2f}s: {str(e)[:50]}...')
        d_flat = None
    
    # QPE implementation
    print('\n' + '*' * 80)
    print('2 QUANTUM PHASE ESTIMATION (shorModule_qpe.py)')
    print('*' * 80)
    print('   Architecture: Two-register (counting 12 + work 6 + ancilla 2)')
    print('   Period Finding: Quantum phase estimation + QFT + continued fractions')
    print('   Status: RUNNING...\n')
    
    time2_start = time.time()
    try:
        sk_qpe = shorModule_qpe.shor_algorithm(pk)
        time2_end = time.time()
        time2_elapsed = time2_end - time2_start
        
        if sk_qpe and sk_qpe[0] > 0:
            print(f'\n SUCCESS in {time2_elapsed:.2f}s')
            d_qpe = sk_qpe[0]
        else:
            print(f'\n FAILED in {time2_elapsed:.2f}s')
            d_qpe = None
    except Exception as e:
        time2_end = time.time()
        time2_elapsed = time2_end - time2_start
        print(f'\n ERROR in {time2_elapsed:.2f}s: {str(e)[:50]}...')
        d_qpe = None
    
    # Summary
    print('\n' + '=' * 80)
    print('SUMMARY')
    print('=' * 80)
    print(f'Classical-Hybrid: {"SUCCESS" if d_flat else "FAILED":20} ({time1_elapsed:.2f}s)')
    print(f'QPE-Based:        {"SUCCESS" if d_qpe else "FAILED":20} ({time2_elapsed:.2f}s)')
    
    # Choose best result
    if d_flat:
        print(f'\nUsing CLASSICAL-HYBRID result (more reliable on simulator)')
        return sk_flat
    elif d_qpe:
        print(f'\nUsing QPE-BASED result (fallback)')
        return sk_qpe
    else:
        print(f'\nBoth methods failed! Returning original key...')
        return [pk[0], pk[1]]


def period(backend, a: int, N: int, method='qpe'):
    '''
    Period-finding wrapper for direct access.
    
    Args:
        backend: Quantum backend
        a: Base
        N: Modulus
        method: 'flat' or 'qpe'
    
    Returns:
        r: Period
    '''
    
    if method == 'flat':
        return shorModule_flat.period(backend, a, N)
    elif method == 'qpe':
        return shorModule_qpe.period(backend, a, N)
    else:
        raise ValueError(f"Unknown method: {method}")


def shors_breaker(backend, N, method='qpe'):
    '''
    Factoring wrapper for direct access.
    
    Args:
        backend: Quantum backend
        N: Modulus to factor
        method: 'flat' or 'qpe'
    
    Returns:
        (p, q): Factors
    '''
    
    if method == 'flat':
        return shorModule_flat.shors_breaker(backend, N)
    elif method == 'qpe':
        return shorModule_qpe.shors_breaker(backend, N)
    else:
        raise ValueError(f"Unknown method: {method}")
