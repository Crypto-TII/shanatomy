import sys
import bitpy as bp

# r = desired round
r = sys.argv[1]

system = bp.get_string('structures/gf2/sha_1_separated.txt')
equations = system.split('\n')
last = list(filter(lambda x: x[0: 7] == 'T00' + r + '31', equations))[0]
equations = equations[0: equations.index(last) + 1]
xors = list(filter(lambda x: '+' in x, equations))
ands = list(filter(lambda x: '*' in x, equations))
bp.store_string('structures/gf2/sha_1_' + r + '.txt', '\n'.join(ands + xors))

