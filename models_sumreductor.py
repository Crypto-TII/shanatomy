import sys
import sympy
import bitpy as bp

def simplify_sumalg(wl, addition, depth):
    steps = addition.split('\n')
    for i in range(wl - 1):
        if i not in range(depth, wl - 1, depth + 1):
            sides = steps[i].split('=')
            for j in range(2 * wl - 1):
                steps[j] = steps[j].replace(sides[0], '(' + sides[1] + ')')
    addition = list(filter(lambda x: x[3] == '=', steps[1:]))
    return '\n'.join(addition)

wl = int(sys.argv[1])
depth = int(sys.argv[2])
K_depth = int(sys.argv[3])
addition = bp.get_string('models/equations/addition.txt')
addition_K0 = bp.get_string('models/equations/addition_K0.txt')
addition_K1 = bp.get_string('models/equations/addition_K1.txt')
addition_K2 = bp.get_string('models/equations/addition_K2.txt')
addition_K3 = bp.get_string('models/equations/addition_K3.txt')

new_addition = simplify_sumalg(wl, addition, depth)
new_addition_K0 = simplify_sumalg(wl, addition_K0, K_depth)
new_addition_K1 = simplify_sumalg(wl, addition_K1, K_depth)
new_addition_K2 = simplify_sumalg(wl, addition_K2, K_depth)
new_addition_K3 = simplify_sumalg(wl, addition_K3, K_depth)

bp.store_string('models/equations/addition' + str(depth) + '.txt', new_addition)
bp.store_string('models/equations/addition' + str(K_depth) + '_K0.txt', new_addition_K0)
bp.store_string('models/equations/addition' + str(K_depth) + '_K1.txt', new_addition_K1)
bp.store_string('models/equations/addition' + str(K_depth) + '_K2.txt', new_addition_K2)
bp.store_string('models/equations/addition' + str(K_depth) + '_K3.txt', new_addition_K3)

