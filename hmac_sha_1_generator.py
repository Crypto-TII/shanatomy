''' This module construct a bit model of HMAC-SHA-1

    System Arguments
    ----------------
    wl : int
        the word length
    key_string : str
        the string to use as password
'''

import re
import sys
import bitpy as bp

## data retrieve

wl = int(sys.argv[1])
value = sys.argv[2]
key_string = sys.argv[3]
key_length = len(key_string)

system = bp.get_string('./structures/sha_1_handy.txt')
system0 = system1 = system2 = system3 = system

H = bp.get_words('H.txt')
key = [bp.bit('K' + bp.fi(0) + bp.fi(i // wl), wl - 1 - i % wl)\
        for i in range(wl * 16)]

## system0

ipad = [0x36363636] * 16
k = 0
for i in range(key_length):
    k = k << 8 ^ ord(key_string[i])
k <<= (512 - 8 * key_length)
W = [(k >> (15 - i) * 32 ^ ipad[i]) & 0xffffffff for i in range(16)]

for i in range(len(H)):
    for j in range(wl):
        system0 = system0.replace(bp.bit('H_' + bp.fi(i), j),\
                str(bool(H[i] >> j & 1)).lower())

system0 = system0.replace('_', bp.fi(0))
system0 = bp.simplify_across(system0)
bp.store_string('./structures/hmac_sha_1_00.txt', system0)

system0 = bp.xor_in_standard_syntax(system0)
system0 = bp.not_in_python_syntax(system0)
for i in range(16):
    for j in range(wl):
        system0 = system0.replace(bp.bit('W' + bp.fi(0) + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)))

## system1

W = bp.words_from_string(wl, value)
W[15] = 0x00000230
for i in range(len(W)):
    for j in range(wl):
        system1 = system1.replace(bp.bit('W_' + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)).lower())

system1 = system1.replace('H_', 'Z' + bp.fi(0))
system1 = system1.replace('_', bp.fi(1))
system1 = bp.simplify_across(system1)
bp.store_string('./structures/hmac_sha_1_01.txt', system1)

system1 = bp.xor_in_standard_syntax(system1)
system1 = bp.not_in_python_syntax(system1)

## system2

opad = [0x5c5c5c5c] * 16
W = [(k >> (15 - i) * 32 ^ opad[i]) & 0xffffffff for i in range(16)]

for i in range(len(H)):
    for j in range(wl):
        system2 = system2.replace(bp.bit('H_' + bp.fi(i), j),\
                str(bool(H[i] >> j & 1)).lower())

system2 = system2.replace('_', bp.fi(2))
system2 = bp.simplify_across(system2)
bp.store_string('./structures/hmac_sha_1_02.txt', system2)

system2 = bp.xor_in_standard_syntax(system2)
system2 = bp.not_in_python_syntax(system2)
for i in range(16):
    for j in range(wl):
        system2 = system2.replace(bp.bit('W' + bp.fi(2) + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)))

## system3

W = [0] * 16
W[5] = 0x80000000
W[15] = 0x000002a0
for i in range(5, 16):
    for j in range(wl):
        system3 = system3.replace(bp.bit('W_' + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)).lower())
for i in range(5):
    for j in range(wl):
        system3 = system3.replace(bp.bit('W_' + bp.fi(i), j),\
                bp.bit('Z' + bp.fi(1) + bp.fi(i), j))

system3 = system3.replace('H_', 'Z' + bp.fi(2))
system3 = system3.replace('_', bp.fi(3))
system3 = bp.simplify_across(system3)
bp.store_string('./structures/hmac_sha_1_03.txt', system3)

system3 = bp.xor_in_standard_syntax(system3)
system3 = bp.not_in_python_syntax(system3)

## testing

hmac_sha_1 = '\n'.join((system0, system1, system2, system3))

exec(hmac_sha_1)

Z = [0] * 5
for i in range(wl):
    Z[0] ^= eval(bp.bit('Z' + bp.fi(3) + bp.fi(0), i)) << i
    Z[1] ^= eval(bp.bit('Z' + bp.fi(3) + bp.fi(1), i)) << i
    Z[2] ^= eval(bp.bit('Z' + bp.fi(3) + bp.fi(2), i)) << i
    Z[3] ^= eval(bp.bit('Z' + bp.fi(3) + bp.fi(3), i)) << i
    Z[4] ^= eval(bp.bit('Z' + bp.fi(3) + bp.fi(4), i)) << i

digest = [f'{Z[i]:08x}' for i in range(5)]
print(''.join(digest))

