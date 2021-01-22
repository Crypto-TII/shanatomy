import re
import random
import bitpy as bp

system = bp.get_string('structures/gf2/sha_1_gf2.txt')
equations = system.split('\n')
system_separated = []
ind = 0
for i in range(len(equations)):
    prods = re.findall(r'[A-Za-z][0-9]{6}\*[A-Za-z][0-9]{6}', equations[i][8:])
    if len(prods) > 0:
        if '+' in equations[i]:
            for j in range(len(prods)):
                system_separated += [f'q{ind:06}=' + prods[j]]
                equations[i] = equations[i].replace(prods[j], f'q{ind:06}')
                ind += 1
            system_separated += [equations[i]]
        else:
            system_separated += [equations[i]]
    else:
        system_separated += [equations[i]]
bp.store_string('structures/gf2/sha_1_separated.txt', '\n'.join(system_separated))

