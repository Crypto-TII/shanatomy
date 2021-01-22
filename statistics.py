import sys
import re
import bitpy as bp
from collections import Counter

to_be_analized = sys.argv[1]
system = bp.get_string(to_be_analized)

if '=' in system:
    eoc = 'equations'
else:
    eoc = 'clauses'

if ('+' in system) or ('*' in system):
    boa = 'algebraic'
else:
    boa = 'boolean'
    system = bp.xor_in_standard_syntax(system)
print('\n*** System of ' + boa + ' ' + eoc + ' ***\n')

n_of_lines = str(len(system.split('\n')))
print('Number of lines: ' + n_of_lines + '\n')

if boa == 'algebraic':
    op_dict = dict(Counter(re.findall(r'[+*]', system)))
    for op in op_dict:
        print(op + ': ' + str(op_dict[op]))
elif boa == 'boolean':
    op_dict = dict(Counter(re.findall(r'[&|~\^]', system)))
    for op in op_dict:
        print(op + ': ' + str(op_dict[op]))

variables = set(re.findall(r'[A-Za-z][0-9]{6}', system))
print('\nTotal variables: ' + str(len(variables)) + '\n')
var_dict = dict(Counter(re.findall(r'[A-Za-z][0-9]{6}', system)))
var_dict_values = set(list(var_dict.values()))
print('variables times')
for i in var_dict_values:
    num_of_vars = len([key for key,value in var_dict.items() if value == i])
    print('{:>9}'.format(str(num_of_vars)) + ' ' + str(i))

