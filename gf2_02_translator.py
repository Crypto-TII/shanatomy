import sys
import bitpy as bp

def sum_to_xor(expr):
    variables = expr.split('+')
    if variables[-1] == '1':
        variables = variables[:-1]
        variables[-1] = '~' + variables[-1]
    variables = ','.join(variables)
    return variables.join(('Xor(', ')'))

to_translate = sys.argv[1]
translated = sys.argv[2]

system = bp.get_string(to_translate)
system = system.replace('*', '&')
equations = system.split('\n')
for i in range(len(equations)):
    if '+' in equations[i]:
        equations[i] = equations[i][:8] + sum_to_xor(equations[i][8:])
system = '\n'.join(equations)
xor_ext_form = bp.to_cnf(system)
bp.store_string(translated, xor_ext_form)

