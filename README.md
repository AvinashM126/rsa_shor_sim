# RSA_SHOR_Simulator

This repository provides a Python-based instructional implementation of:

- RSA key generation, encryption, and decryption
- Supporting classical arithmetic procedures (prime generation, GCD, modular inverse)
- A Qiskit-based simulation workflow motivated by Shor's algorithm for recovering factors of small RSA moduli

## Project Goal

The primary objective of this project is to offer an educational simulation environment for studying RSA and for illustrating how quantum period-finding concepts can be applied to factor small RSA-style examples under simulator constraints.

## Setup and Prerequisites

All installation, environment initialization, and prerequisite instructions are maintained in:

- [Prerequisite and context guide](documentations/prerequisite_requirements.md)

This document should be treated as the authoritative reference for preparing both the host system and Python environment.

## Repository Structure

```text
RSA_SHOR_Simulator/
├── RSA_SHOR_main.py
├── run.bat
├── batch_scripts/
│   ├── setup.bat
│   └── requirements.txt
├── documentations/
│   ├── breaker_flow.md
│   ├── code_flow.md
│   └── prerequisite_requirements.md
└── module_scripts/
    ├── arithmeticModule.py
    ├── rsaModule.py
  	├── shorModule.py
  	├── shorModule_flat.py
  	└── shorModule_qpe.py
```

## Running the Simulator

After completing the documented setup procedure, execute:

```bat
python RSA_SHOR_main.py
```

At runtime, the script performs the following sequence:

1. Generates Lorem Ipsum text as sample plaintext
2. Generates RSA key pairs (`p`, `q`, `n`, `e`, `d`)
3. Applies RSA encryption and decryption
4. Lets you choose Shor breaker mode (`flat`, `qpe`, or `auto`)
5. Executes the selected breaker path on a simulation backend for small key sizes
6. Applies automatic fallback for unsupported QPE modulus sizes
7. Verifies equivalence between original and recovered plaintext

## Quick Demo

Illustrative console workflow:

1. Launch the program with `python RSA_SHOR_main.py`
2. Provide a small bit size when prompted (for example, `8`)
3. Inspect the reported RSA parameters and encryption/decryption outputs
4. Select implementation mode (`1=flat`, `2=qpe`, `3=auto`)
5. Observe the factor recovery and private-key reconstruction
6. Confirm that the final verification statement evaluates to `True`

## Important Notes

- The script is configured for Shor flow by default (`choice_shor = True`).
- The `input_bits` prompt refers to the bit-length of each prime (`p` and `q`), not modulus bit-length.
- RSA modulus size is approximately `2 * input_bits`.
- QPE mode is currently constrained by `WORK_QUBITS` in `module_scripts/shorModule_qpe.py`.
- If QPE is selected for an unsupported modulus size, execution falls back to `flat` mode.
- This repository is designed for instructional use and does not represent a production-grade cryptographic implementation.

## Known Limitations

- The implementation targets demonstration-scale inputs and is not suitable for real RSA security parameters.
- Quantum behavior is emulated via Qiskit Aer and is not executed on physical quantum hardware.
- Computational cost increases with input size and simulation-circuit overhead.

## Compatibility

- Primary execution flow is Windows-oriented via `run.bat` and `batch_scripts/setup.bat`.
- Recommended Python version is 3.10 or later.
- Dependency specifications are maintained in `batch_scripts/requirements.txt`.

## Architecture Flow

```mermaid
flowchart LR
  A[Generate RSA keys] --> B[Encrypt lorem message]
  B --> C[Choose breaker mode flat qpe auto]
  C --> D[Router dispatch in shorModule.py]
  D --> E[Recover p and q]
  E --> F[Reconstruct private key d]
  F --> G[Decrypt and verify plaintext match]
```

### Shor Module Architecture

- `module_scripts/shorModule.py`
  - Router/dispatcher only
  - Routes calls to isolated implementations (`flat`, `qpe`, `auto`)
- `module_scripts/shorModule_flat.py`
  - Classical-hybrid implementation
  - More reliable under simulator constraints
- `module_scripts/shorModule_qpe.py`
  - QPE-style implementation with counting/work/ancilla registers
  - Includes modulus-size compatibility guard based on `WORK_QUBITS`

The architecture diagram above provides the high-level pipeline. For implementation-level flow references focused on the quantum section and breaker decision logic, use the following add-ons:

- [Period Function Code Flow Add-on](documentations/code_flow.md)
- [Shor Breaker Flow Add-on](documentations/breaker_flow.md)

## What This Project Demonstrates

1. End-to-end RSA key-generation and encryption/decryption workflow
2. Core arithmetic primitives relevant to public-key cryptography (GCD and modular inverse)
3. A quantum-simulation pathway for factoring small RSA modulus values
4. Reconstruction of a private key from recovered factors

## Module Summary

- `module_scripts/arithmeticModule.py`

  - Primality-testing helpers
  - Prime generation
  - Extended Euclidean Algorithm
  - Modular inverse
  - Naive factorization utility
- `module_scripts/rsaModule.py`

  - RSA keypair generation
  - RSA encryption/decryption routines
  - RSA parameter reporting
- `module_scripts/shorModule.py`

  - Router/dispatcher for Shor implementation selection
  - `shor_algorithm(pk, method='auto')` entrypoint
  - Comparison mode (`auto`) for flat vs qpe
- `module_scripts/shorModule_flat.py`

  - Classical-hybrid Shor breaker path
  - Flat-register period and factor recovery flow
- `module_scripts/shorModule_qpe.py`

  - QPE-based Shor breaker path
  - Counting/work register flow with continued fraction post-processing
  - QPE compatibility guard for modulus bit-length
