''' This module test the correctness of SHA-1 system. It also store a
    map of block used and the 82 states of SHA-1 function. These files
    are compulsory to mount the SAT solver attack. So, before to
    construct the CNF for SAT solver, please run this module.

    System Arguments
    ----------------
    wl : int
        the word length of the used
    mode : int
        0 from string
        1 from file
    string : str
        if mode == '0', the string to be hashed
        if mode == '1', the name of the file from which take the block
    file_id
        an identification for the files 'block' and 'states'
        (consider an integer)
'''

import sys
import re
import bitpy as bp

wl = int(sys.argv[1])
mode = sys.argv[2]
string = sys.argv[3]
file_id = sys.argv[4]

if mode == '0':
    W = bp.words_from_string(wl, string)
else:
    if mode == '1':
        W = bp.get_words(string)

system = bp.get_string('./structures/sha_1.txt')
system = bp.xor_in_standard_syntax(system)
system = bp.not_in_python_syntax(system)

#K = bp.get_words('K.txt')
H = bp.get_words('H.txt')

#for i in range(len(K)):
#    for j in range(wl):
#        system = system.replace(bp.bit('K' + bp.fi(i), j),\
#                str(bool(K[i] >> j & 1)))
for i in range(len(H)):
    for j in range(wl):
        system = system.replace(bp.bit('H' + bp.fi(0) + bp.fi(i), j),\
                str(bool(H[i] >> j & 1)))
for i in range(len(W)):
    for j in range(wl):
        system = system.replace(bp.bit('W' + bp.fi(0) + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)))

exec(system)

W += [0] * 64
for i in range(16, 80):
    for j in range(wl):
        W[i] ^= eval(bp.bit('W' + bp.fi(0) + bp.fi(i), j)) << j
bp.store_words('./maps/block_' + file_id + '.txt', wl, W)

states = [0] * 82
for i in range(81):
    for j in range(wl):
        states[i] ^= eval(bp.bit('A' + bp.fi(0) + bp.fi(i), j)) << j + 4 * wl
        states[i] ^= eval(bp.bit('B' + bp.fi(0) + bp.fi(i), j)) << j + 3 * wl
        states[i] ^= eval(bp.bit('C' + bp.fi(0) + bp.fi(i), j)) << j + 2 * wl
        states[i] ^= eval(bp.bit('D' + bp.fi(0) + bp.fi(i), j)) << j + wl
        states[i] ^= eval(bp.bit('E' + bp.fi(0) + bp.fi(i), j)) << j
for j in range(wl):
    states[81] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(0), j)) << j + 4 * wl
    states[81] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(1), j)) << j + 3 * wl
    states[81] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(2), j)) << j + 2 * wl
    states[81] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(3), j)) << j + wl
    states[81] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(4), j)) << j
bp.store_words('./maps/states_' + file_id + '.txt', wl * 5, states)

