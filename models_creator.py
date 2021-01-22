''' This module creates models to be used in creation of SHA-1 system.

    System Arguments
    ----------------
    wl : int
        the length of the word to be used
    rW : int
        the amount of the rotation for scheduling
    rB : int
        the amount of the rotation in relabeling third word
'''

import sys
import sympy
import bitpy as bp

def relabel_model(length, new, old, r):
    w0 = bp.word(length, new)
    w1 = bp.word(length, old, r)
    return '\n'.join(bp.wequal(w0, w1))

wl = int(sys.argv[1])
rW = int(sys.argv[2])
rB = int(sys.argv[3])

# Relabeling states

r = [''] * 5
r[0] = relabel_model(wl, 'Aa', 'Tb', 0)
r[1] = relabel_model(wl, 'Ba', 'Ab', 0)
r[2] = relabel_model(wl, 'Ca', 'Bb', rB)
r[3] = relabel_model(wl, 'Da', 'Cb', 0)
r[4] = relabel_model(wl, 'Ea', 'Db', 0)
bp.store_string('./models/equations/state_relabel.txt', '\n'.join(r))

# Round functions f

F = bp.word(wl, 'F')
B = bp.word(wl, 'B')
C = bp.word(wl, 'C')
D = bp.word(wl, 'D')
f0 = bp.wequal(F, bp.wor([bp.wand([B, C], 1), bp.wand([bp.wnot(B), D], 1)]))
bp.store_string('./models/equations/f0.txt', '\n'.join(f0))
f1 = bp.wequal(F, bp.wxor([B, C, D]))
bp.store_string('./models/equations/f1.txt', '\n'.join(f1))
f2 = bp.wequal(F, bp.wor(\
        [bp.wand([B, C], 1), bp.wand([B, D], 1), bp.wand([C, D], 1)]))
bp.store_string('./models/equations/f2.txt', '\n'.join(f2))

# Message scheduling

W0 = bp.word(wl, 'Wa')
W1 = bp.word(wl, 'Wb', rW)
W2 = bp.word(wl, 'Wc', rW)
W3 = bp.word(wl, 'Wd', rW)
W4 = bp.word(wl, 'We', rW)
expansion = bp.wequal(W0, bp.wxor([W1, W2, W3, W4]))
bp.store_string('./models/equations/expansion.txt', '\n'.join(expansion))

# Addition modulo 2 ^ wl

X = bp.word(wl, 'x')
Y = bp.word(wl, 'y')
C = bp.word(wl - 1, 'c')
Z = bp.word(wl, 'z')
carries = [''] * (wl - 1)
carries[0] = '&'.join((X[0], Y[0]))
for i in range(1, wl - 1):
    carries[i] = ''.join(('(',\
            C[i - 1], '&', X[i], ')|(',\
            C[i - 1], '&', Y[i], ')|(',\
            X[i], '&', Y[i], ')'))
carries = bp.wequal(C, carries)
results = [''] * wl
results[0] = ''.join(('Xor(', X[0], ',', Y[0], ')'))
for i in range(1, wl):
    results[i] = ''.join(('Xor(', X[i], ',', Y[i], ',', C[i - 1], ')'))
results = bp.wequal(Z, results)
bp.store_string('./models/equations/addition.txt',\
        '\n'.join(carries + results))

# Addition modulo 2 ^ wl with the first part of the K constant

K = bp.get_words('K.txt')
K_additions = [''] * len(K)
for i in range(len(K)):
    new_addition = '\n'.join(carries + results)
    for j in range(wl):
        new_addition = new_addition.replace(bp.bit('y', j),\
                str(bool(K[i] >> j & 1)).lower())
    new_addition = new_addition.split('\n')
    for j in range(wl - 1):
        new_addition[j] = ''.join((new_addition[j][0: 4],\
                str(sympy.to_cnf(new_addition[j][4:], True))))
    for j in range(wl - 1, 2 * wl - 1):
        new_addition[j] = ''.join((new_addition[j][0: 4],\
                bp.reduce_xor(new_addition[j][4:], r'~?[xyc][0-9]{2}')))
    K_additions[i] = '\n'.join(new_addition).replace(' ', '')
for i in range(len(K)):
    bp.store_string('./models/equations/addition_K' + str(i) + '.txt',\
            K_additions[i])

