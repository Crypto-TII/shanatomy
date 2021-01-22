import sys
import bitpy as bp

wl = int(sys.argv[1])
system = bp.get_string('./structures/sha_1.txt')

system = bp.simplify_across(system)

bp.store_string('./structures/sha_1_no_assignments.txt', system)

H = bp.get_words('H.txt')
for i in range(len(H)):
    for j in range(wl):
        system = system.replace(bp.bit('H' + bp.fi(0) + bp.fi(i), j),\
                str(bool(H[i] >> j & 1)).lower())

system = bp.simplify_across(system)

bp.store_string('./structures/sha_1_first_block.txt', system)

W = bp.words_from_string(wl, "Chiara")

system = bp.xor_in_standard_syntax(system)
system = bp.not_in_python_syntax(system)

for i in range(len(W)):
    for j in range(wl):
        system = system.replace(bp.bit('W' + bp.fi(0) + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)))

exec(system)

Z = [0] * 5
for i in range(wl):
    Z[0] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(0), i)) << i
    Z[1] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(1), i)) << i
    Z[2] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(2), i)) << i
    Z[3] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(3), i)) << i
    Z[4] ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(4), i)) << i

digest = (f'{Z[i]:08x}' for i in range(5))
print(''.join(digest))

