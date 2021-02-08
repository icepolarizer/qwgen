#!/usr/bin/env python3

# Dependency: qiskit, pyperclip

def warn (* args, **kwargs):
    pass
import warnings
warnings.warn = warn

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clipboard", action="store_true",
                    help="paste to the clipboard")
parser.add_argument("-l", "--length", type=int,
                    help="password length")
args = parser.parse_args()

import string, math
from qiskit import *

import pyperclip


table = string.ascii_uppercase + string.ascii_lowercase + string.digits
circ = QuantumCircuit(6)

for q in range(6):
    circ.h(q)

circ.measure_all()

backend_sim = Aer.get_backend('qasm_simulator')

def rand_int():
    rand = 62
    while rand > 61:
        job_sim = execute(circ, backend_sim, shots=1)
        result_sim = job_sim.result()

        count = result_sim.get_counts(circ)
        bits = max(count, key=lambda i: count[i])[:6]
        rand = int(bits, 2)
    return rand

pwlen = 8
if args.length:
    pwlen = args.length

if args.clipboard:
    pyperclip.copy(''.join(table[rand_int()] for _ in range(pwlen)))
    print("Random password copied to clipboard")
else:
    for i in range(20):
        for j in range(8):
            pw = ''.join(table[rand_int()] for _ in range(pwlen))
            print(pw+' ', end='')
        print('\n', end='')
