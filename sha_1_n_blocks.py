import sys
import re 
import bitpy as bp

wl = int(sys.argv[1])
n = int(sys.argv[2])

systems = [''] * n
systems[0] = bp.get_string('./structures/sha_1.txt')
system = bp.get_string('./structures/sha_1_handy.txt')
for i in range(1, n):
    systems[i] = system.replace('H_', 'Z' + bp.fi(i - 1))
    systems[i] = systems[i].replace('_', bp.fi(i))

sha_1 = '\n'.join(systems)
bp.store_string('./structures/sha_1_' + str(n) + '_blocks.txt', sha_1)
H = bp.get_words('H.txt')
for i in range(len(H)):
    for j in range(wl):
        sha_1 = sha_1.replace(bp.bit('H' + bp.fi(0) + bp.fi(i), j),\
                str(bool(H[i] >> j & 1)))

test_check = input('Do you want to test it? [y/n] ')
if test_check == 'y':
    low = 56 + (n - 2) * 64
    high = 119 + (n - 2) * 64
    string = input('Type a string (escapes not allowed) with a x number of ' +\
            'chars such that ' + str(low) + ' ≤ x ≤ ' + str(high) + '.\n')
    W = bp.words_from_string(32, string)
    for i in range(n):
        for j in range(16):
            for k in range(wl):
                sha_1 = sha_1.replace(bp.bit('W' + bp.fi(i) + bp.fi(j), k),\
                        str(bool(W[i * 16 + j] >> k & 1)))
    
    sha_1 = bp.xor_in_standard_syntax(sha_1)
    sha_1 = bp.not_in_python_syntax(sha_1)
    
    exec(sha_1)
    
    digest = 0
    for i in range(wl):
        digest ^= eval(bp.bit('Z' + bp.fi(n - 1) + bp.fi(0), i)) << i + 4 * wl
        digest ^= eval(bp.bit('Z' + bp.fi(n - 1) + bp.fi(1), i)) << i + 3 * wl
        digest ^= eval(bp.bit('Z' + bp.fi(n - 1) + bp.fi(2), i)) << i + 2 * wl
        digest ^= eval(bp.bit('Z' + bp.fi(n - 1) + bp.fi(3), i)) << i + wl
        digest ^= eval(bp.bit('Z' + bp.fi(n - 1) + bp.fi(4), i)) << i
    
    print('SHA-1 digest is: ' + f'{digest:040x}')
else:
    if test_check == 'n':
        print('SHA-1 system saved in file: structures/sha_1_' + str(n) +\
                '_blocks.txt')
    else:
        print('Error, just type a char (s or n).')

