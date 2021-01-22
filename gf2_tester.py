import sys
import re
import bitpy as bp

system_path = sys.argv[1]
system = bp.get_string(system_path)
system = system.replace('*', '&')
system = system.replace('+', '^')

string = sys.argv[2]
W = bp.words_from_string(32, string)

for i in range(len(W)):
    for j in range(32):
        system = system.replace(bp.bit('W' + bp.fi(0) + bp.fi(i), j),\
                str(bool(W[i] >> j & 1)))

exec(system)

digest = 0
for j in range(32):
    digest ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(0), j)) << j + 128
    digest ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(1), j)) << j + 96
    digest ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(2), j)) << j + 64
    digest ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(3), j)) << j + 32
    digest ^= eval(bp.bit('Z' + bp.fi(0) + bp.fi(4), j)) << j
print(f'{digest:040x}')

