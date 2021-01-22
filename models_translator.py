import sys
import bitpy as bp

addition_depth = int(sys.argv[1])
addition_K_depth = int(sys.argv[2])

## functions F to cnf

for i in range(3):
    model = bp.get_string('./models/equations/f' + str(i) + '.txt')
    cnf = bp.to_total_cnf(model)
    bp.store_string('./models/cnf/f' + str(i) + '.txt', cnf)

## expansion to cnf

model = bp.get_string('./models/equations/expansion.txt')
cnf = bp.to_total_cnf(model)
bp.store_string('./models/cnf/expansion.txt', cnf)

## addition to cnf

if addition_depth != 0:
    model = bp.get_string('./models/equations/addition' + str(addition_depth) + '.txt')
    cnf = bp.to_total_cnf(model)
    bp.store_string('./models/cnf/addition' + str(addition_depth) + '.txt', cnf)

## addition with K to cnf

if addition_K_depth != 0:
    for i in range(4):
        model = bp.get_string('./models/equations/addition' + str(addition_K_depth) + '_K' + str(i) + '.txt')
        cnf = bp.to_total_cnf(model)
        bp.store_string('./models/cnf/addition' + str(addition_K_depth) + '_K' + str(i) + '.txt', cnf)

