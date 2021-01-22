import sys
import re
import bitpy as bp

wl = int(sys.argv[1])
round_to_attack = int(sys.argv[2])
file_id = sys.argv[3]
preimage_length = int(sys.argv[4])
cnf = sys.argv[5]

system = bp.get_string(cnf)
clauses = system.split('\n')
last_carry = 'g' + bp.fi(0) + bp.fi(round_to_attack - 1) + bp.fi(wl - 2)
last_clause = list(filter(lambda x: last_carry in x, clauses))[-1]
system = '\n'.join(clauses[0: clauses.index(last_clause) + 1])

states = bp.get_words('./maps/states_' + file_id + '.txt')
for i in range(5):
    states[i] = states[round_to_attack - 4 + i] >> (wl * 4)

for i in range(5):
    for j in range(wl):
        system = system.replace(\
                bp.bit('T' + bp.fi(0) + bp.fi(round_to_attack - 5 + i), j),\
                str(bool(states[i] >> j & 1)).lower())

fixed, system = bp.fix_bits(wl, system, preimage_length)
system = bp.cnf_simplify_across(system)
system = system.replace('~', '-')
system = system.replace('|', ' ')
system = system.replace('Xor(', 'x')
system = system.replace(')', '')
system = system.replace(',', ' ')
system = system.replace('\n', ' 0\n') + ' 0'
clauses = system.split('\n')
variables = []
for i in range(len(clauses)):
    vars_temp = re.findall(r'[A-Za-z][0-9]{6}', clauses[i])
    for v in vars_temp:
        if v not in variables:
            variables += [v]
for i in range(len(variables)):
    system = system.replace(variables[i], str(i + 1))
num_of_variables = len(variables)
num_of_clauses = len(system.split('\n'))
sat_form = 'p cnf ' + str(num_of_variables) + ' ' + str(num_of_clauses) + '\n'
sat_form += system
bp.store_string('./temp/fixed_' + file_id + '.txt', '\n'.join(fixed))
bp.store_string('./temp/variables_' + file_id + '.txt', '\n'.join(variables))
bp.store_string('./temp/to_solve_' + file_id + '.cnf', sat_form)

