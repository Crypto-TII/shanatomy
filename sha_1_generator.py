''' This module creates a SHA-1 system representation bit by bit.
'''

import sys
import re
import bitpy as bp

def initial_relabel(wl):
    state_words = ['A', 'B', 'C', 'D', 'E']
    initial_relabels = [''] * 5
    for i in range(5):
        w0 = bp.word(wl, state_words[i] + bp.fi(0))
        w1 = bp.word(wl, 'H' + bp.fi(i))
        relabels = bp.wequal(w0, w1)
        initial_relabels[i] = '\n'.join(relabels)
    return '\n'.join(initial_relabels)

def state_relabel_ind(model, i):
    model = model.replace('b', bp.fi(i))
    model = model.replace('a', bp.fi(i + 1))
    return model

def f_ind(f, i):
    i = bp.fi(i)
    f = f.replace('F', 'F' + i)
    f = f.replace('B', 'B' + i)
    f = f.replace('C', 'C' + i)
    f = f.replace('D', 'D' + i)
    return f

def expansion_ind(model, i):
    model = model.replace('a', bp.fi(i))
    model = model.replace('b', bp.fi(i - 3))
    model = model.replace('c', bp.fi(i - 8))
    model = model.replace('d', bp.fi(i - 14))
    model = model.replace('e', bp.fi(i - 16))
    return model

def round_ind(addition_K, addition, wl, rotation_A, i):
    i = bp.fi(i)
    add_K = addition_K.replace('x', 'E' + i)
    add_K = add_K.replace('c', 'a' + i)
    add_K = add_K.replace('z', 'b' + i)
    add_0 = addition.replace('x', 'b' + i)
    add_0 = add_0.replace('y', 'F' + i)
    add_0 = add_0.replace('c', 'c' + i)
    add_0 = add_0.replace('z', 'd' + i)
    add_1 = addition
    add_1 = add_1.replace('x', 'd' + i)
    A = bp.word(wl, 'A' + i, rotation_A)
    for j in range(wl):
        add_1 = add_1.replace('y' + bp.fi(j), A[j])
    add_1 = add_1.replace('c', 'e' + i)
    add_1 = add_1.replace('z', 'f' + i)
    add_2 = addition.replace('x', 'f' + i)
    add_2 = add_2.replace('y', 'W' + i)
    add_2 = add_2.replace('c', 'g' + i)
    add_2 = add_2.replace('z', 'T' + i)
    return '\n'.join((add_K, add_0, add_1, add_2))

def final_addition_ind(addition):
    add_0 = addition.replace('x', 'A80')
    add_0 = add_0.replace('y', 'H00')
    add_0 = add_0.replace('c', 'h00')
    add_0 = add_0.replace('z', 'Z00')
    add_1 = addition.replace('x', 'B80')
    add_1 = add_1.replace('y', 'H01')
    add_1 = add_1.replace('c', 'h01')
    add_1 = add_1.replace('z', 'Z01')
    add_2 = addition.replace('x', 'C80')
    add_2 = add_2.replace('y', 'H02')
    add_2 = add_2.replace('c', 'h02')
    add_2 = add_2.replace('z', 'Z02')
    add_3 = addition.replace('x', 'D80')
    add_3 = add_3.replace('y', 'H03')
    add_3 = add_3.replace('c', 'h03')
    add_3 = add_3.replace('z', 'Z03')
    add_4 = addition.replace('x', 'E80')
    add_4 = add_4.replace('y', 'H04')
    add_4 = add_4.replace('c', 'h04')
    add_4 = add_4.replace('z', 'Z04')
    return "\n".join((add_0, add_1, add_2, add_3, add_4))

f0 = bp.get_string('./models/equations/f0.txt')
f1 = bp.get_string('./models/equations/f1.txt')
f2 = bp.get_string('./models/equations/f2.txt')
expansion = bp.get_string('./models/equations/expansion.txt')
addition = bp.get_string('./models/equations/addition.txt')
addition_K0 = bp.get_string('./models/equations/addition_K0.txt')
addition_K1 = bp.get_string('./models/equations/addition_K1.txt')
addition_K2 = bp.get_string('./models/equations/addition_K2.txt')
addition_K3 = bp.get_string('./models/equations/addition_K3.txt')
relabel = bp.get_string('./models/equations/state_relabel.txt')

wl = int(sys.argv[1])
rotation_A = int(sys.argv[2])
rounds = int(sys.argv[3])

system = [initial_relabel(wl)]
for i in range(0, min(rounds, 16)):
    system += [f_ind(f0, i)]
    system += [round_ind(addition_K0, addition, wl, rotation_A, i)]
    system += [state_relabel_ind(relabel, i)]
for i in range(16, min(rounds, 20)):
    system += [f_ind(f0, i)]
    system += [expansion_ind(expansion, i)]
    system += [round_ind(addition_K0, addition, wl, rotation_A, i)]
    system += [state_relabel_ind(relabel, i)]
for i in range(20, min(rounds, 40)):
    system += [f_ind(f1, i)]
    system += [expansion_ind(expansion, i)]
    system += [round_ind(addition_K1, addition, wl, rotation_A, i)]
    system += [state_relabel_ind(relabel, i)]
for i in range(40, min(rounds, 60)):
    system += [f_ind(f2, i)]
    system += [expansion_ind(expansion, i)]
    system += [round_ind(addition_K2, addition, wl, rotation_A, i)]
    system += [state_relabel_ind(relabel, i)]
for i in range(60, min(rounds, 80)):
    system += [f_ind(f1, i)]
    system += [expansion_ind(expansion, i)]
    system += [round_ind(addition_K3, addition, wl, rotation_A, i)]
    system += [state_relabel_ind(relabel, i)]
if rounds == 80:
    system += [final_addition_ind(addition)]

for i in range(len(system)):
    bits = re.findall(r'[A-Za-z][0-9]{4}', system[i])
    for b in bits:
        system[i] = system[i].replace(b, b[0] + '_' + b[1:])

system = '\n'.join(system)
system0 = system.replace('_', bp.fi(0))

temp, relabels = bp.get_assignments(system0)
bp.store_string('./structures/relabels.txt', '\n'.join(relabels))
bp.store_string('./structures/sha_1.txt', system0)
bp.store_string('./structures/sha_1_handy.txt', system)

