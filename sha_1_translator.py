''' This module takes SHA-1 system and create two files containing the 
    CNF form. The first (sha_1_total_cnf.txt) contains the ordinary CNF 
    form, the second (sha_1_cnf.txt) contains the version for speed up
    about xor clauses in CryptoMiniSat.

    PAY ATTENTION
    It could take long time to return.
'''

import sys
import bitpy as bp

preserve_xor = sys.argv[1]
system_file = sys.argv[2]
system = bp.get_string(system_file)

## total

cnf_form = bp.to_total_cnf(system)
bp.store_string('./structures/sha_1_total_cnf.txt', cnf_form)

## preserving xors

if preserve_xor:
    cnf_form = bp.to_cnf(system)
    bp.store_string('./structures/sha_1_cnf.txt', cnf_form)

