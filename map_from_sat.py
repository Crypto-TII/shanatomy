import sys
import bitpy as bp

wl = int(sys.argv[1])
file_id = sys.argv[2]

sol_lines = bp.get_string('./temp/preimage_' + file_id + '.txt').split('\n')
sol_lines = list(filter(lambda x: x[0] == 'v', sol_lines[:-1]))
sol_lines = [x[2:] for x in sol_lines]
sol_lines[-1] = sol_lines[-1][0:-2]
sol_bits = ' '.join(sol_lines)
sol_bits = sol_bits.replace('  ', ' ')
sol_bits = sol_bits.split()

var_lines = bp.get_string('./temp/variables_' + file_id + '.txt').split('\n')
fin_dict = {}
for i in range(len(sol_bits)):
    if var_lines[i][0] == 'W':
        fin_dict[var_lines[i]] = sol_bits[i]

var_lines = bp.get_string('./temp/fixed_' + file_id + '.txt').split('\n')
for i in range(len(var_lines)):
    if var_lines[i][0] == '0':
        fin_dict[var_lines[i][1:]] = '-1'
    else:
        fin_dict[var_lines[i][1:]] = '1'

preimage = ''
for i in range(wl * 16):
    if fin_dict[bp.bit('W' + bp.fi(0) + bp.fi(i // wl),\
            (wl - 1) - i % wl)][0] == '-':
        preimage += '0'
    else:
        preimage += '1'

M1 = int(preimage, base = 2)
W = [0] * 16
for i in range(16):
    W[i] = (M1 >> (15 - i) * wl) & 0xFFFFFFFF
    W[i] = f'{W[i]:08x}'
bp.store_string('./temp/preimage_' + file_id + '.txt', '\n'.join(W))

