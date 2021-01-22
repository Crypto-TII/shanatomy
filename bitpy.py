''' This is the only module created in this project for bit by bit
    manipulation of logical operations between words. The aim of this
    code is to test which are the performance of a SAT solver in
    reversing SHA-1 digest or, at least, one of its states.

    The code is intended just a "classical" library beacuse there is the need
    to cooperate with SAT solvers. In order to do that, this software can
    generate not only the well known DIMACS standard, but also the slight
    different form with xor extension specifically for CryptoMiniSat.

    Remarks:
    - the MSB is indexed by 31;
    - as far as possible all is inteded in big endian representation;
    - through the whole project the most important variable is wl, it
      is the word length, e.g., in SHA-1 equal to 32.
'''

import random
import re
import math
import sympy

## base functions

def store_string(name, s):
    '''
    Parameters
    ----------
    name : string
        the name of the file in which store the string take care of the
        existence of the path if you plan to save it in different
        directory from the working one
    s : string
        the string to store
    '''
    fp = open(name, 'wt')
    fp.write(s)
    fp.close()

def get_string(name):
    '''
    Parameters
    ----------
    name : str
        the name of the file from which get the text
    Returns
    -------
    str
        file content

    '''
    fp = open(name, 'rt')
    s = fp.read()
    fp.close()
    return s

def store_words(name, wl, words):
    '''
    Parameters
    ----------
    name : string
        the name of the file in which store words
    wl : int
        word length in bits
    words : list of int
        list of integers to store in big endian
    '''
    f = '{:0' + str(math.ceil(wl / 4)) + 'x}'
    fp = open(name, 'wt')
    for w in words:
        fp.write(f.format(w) + '\n')
    fp.close()

def get_words(name):
    '''
    Parameters
    ----------
    name : str
        the name of the file from which get words
    Returns
    -------
    list
        usually words or states in big endian

    '''
    fp = open(name, 'rt')
    ints = fp.read().splitlines()
    fp.close()
    return [int(i, base = 16) for i in ints]

def fi(i):
    '''
    Parameters
    ----------
    i : int
        the integer to be formatted
    Returns
    -------
    str
        the string representing the integer in fixed length of 2 chars
    Examples
    --------
        >>> fi(7)
        '07'
        >>> fi(11)
        '11'
    '''
    return f'{i:02}'

def bit(bit_id, i):
    '''
    Parameters
    ----------
    bit_id : str
        identifier of the bit
    i : int
        index to append to bit_id, i.e., the poisition in the word
    Returns
    -------
    str
        representation of the bit
    Examples
    --------
        >>> bit('a0204', 3)
        'a020403'
    '''
    return ''.join((bit_id, fi(i)))

def word(length, bit_id, r = 0):
    '''
    Parameters
    ----------
    length : int
        bit length of the word
    bit_id : str
        the name of the word
    r : int
        amount of the rotation
    Returns
    -------
    list of str
        representation of the word
    Examples
    --------
        >>> word(8, 'a')
        ['a00', 'a01', 'a02', 'a03', 'a04', 'a05', 'a06', 'a07']
        >>> word(8, 'a', 3)
        ['a05', 'a06', 'a07', 'a00', 'a01', 'a02', 'a03', 'a04']

    '''
    w = [bit(bit_id, i) for i in range(length)]
    w = w[-r:] + w[:-r]
    return w

## operations with words

def wand(words, p = 0):
    w = [''] * len(words[0])
    for i in range(len(words[0])):
        w[i] = '&'.join((word[i] for word in words))
    return [w[i].join((p * '(', p * ')')) for i in range(len(w))]

def wequal(w0, w1):
    return ['='.join((w0[i], w1[i])) for i in range(len(w0))]

def wnot(word, p = 0):
    w = ['~' + word[i] for i in range(len(word))]
    return [w[i].join((p * '(', p * ')')) for i in range(len(w))]

def wor(words, p = 0):
    w = [''] * len(words[0])
    for i in range(len(words[0])):
        w[i] = '|'.join((word[i] for word in words))
    return [w[i].join((p * '(', p * ')')) for i in range(len(w))]

def wxor(words):
    w = [''] * len(words[0])
    for i in range(len(words[0])):
        w[i] = ','.join((word[i] for word in words))
    return [w[i].join(('Xor(', ')')) for i in range(len(w))]

## testing

def xor_in_standard_syntax(system):
    '''
    Parameters
    ----------
    system : str
        any string, but, here, in particular a system containing the
        expression 'Xor(...)'
    Returns
    -------
    str
        the same string in the input with 'Xor(...)' changed as
        '...^...'
    Examples
    --------
        >>> xor_in_standard_syntax('Xor(f0027,W0027,g0026)')
        '(f0027^W0027^g0026)'
    '''
    xors = re.findall(r'Xor\(.*\)', system)
    for x in xors:
        bits = x[4: -1].split(',')
        bits = '^'.join(bits)
        bits = bits.join(('(', ')'))
        system = system.replace(x, bits)
    return system

def not_in_python_syntax(system):
    '''
    Parameters
    ----------
    system : str
        the representation of any system of boolean expression
    l : int
        amount of the length of the identifying digits
    Returns
    -------
    str
        the system with executable not in Python
    '''
    neg_vars = re.findall(r'~[A-Za-z][0-9]{6}', system)
    for neg_var in neg_vars:
        system = system.replace(neg_var, neg_var[1:].join(('(not ', ')')))
    return system

def words_from_string(wl, string):
    '''
    Parameters
    ----------
    wl : int
        bit length of the word
    string : str
        the string from which getting the block
    Returns
    -------
    list
        list of 16 integers representing the block for hash algorithm
    Examples:
        >>> W=words_from_string(32, '')
        >>> [f'{w:08x}' for w in W]
        ['80000000', '00000000', '00000000', '00000000', '00000000',
        '00000000', '00000000', '00000000', '00000000', '00000000',
        '00000000', '00000000', '00000000', '00000000', '00000000',
        '00000000']
        >>> W=words_from_string(32, 'Chiara')
        >>> [f'{w:08x}' for w in W]
        ['43686961', '72618000', '00000000', '00000000', '00000000',
        '00000000', '00000000', '00000000', '00000000', '00000000',
        '00000000', '00000000', '00000000', '00000000', '00000000',
        '00000030']
    '''
    if string == '':
        return [2 ** (wl - 1)] + [0] * 15
    n = 1 + len(string) // 64
    block = ord(string[0])
    for i in range(1, len(string)):
        block = block << 8 ^ ord(string[i])
    block = block << 1 ^ 1
    pad_length = 16 * wl * n - 8 * len(string) - 1
    block <<= pad_length
    block ^= len(string * 8)
    block_words = [0] * (16 * n)
    mask = 2 ** wl - 1
    for i in range(16 * n):
        block_words[i] = block >> (i * wl) & mask
    return block_words[::-1]

#def block_random(num_of_bits):
#    message = random.getrandbits(num_of_bits)
#    message <<= 512 - num_of_bits
#    message ^= 1 << (511 - num_of_bits)
#    message ^= num_of_bits
#    block = [0] * 16
#    for i in range(16):
#        block[i] = (message >> (15 - i) * 32) & 0xFFFFFFFF
#    return block

## reducing equations

def reduce_xor(xor_expression, regex):
    variables = re.findall(regex, xor_expression)
    xor_expression = xor_expression.replace('True', 'true')
    xor_expression = xor_expression.replace('False', 'false')
    xor_expression = xor_expression.replace('~false', 'true')
    xor_expression = xor_expression.replace('~true', 'false')
    if len(variables) < 2:
        return str(sympy.to_cnf(xor_expression, True))
    number_of_true = len(re.findall(r'true', xor_expression)) % 2
    variables[0] = ('~' * number_of_true) + variables[0]
    variables[0] = variables[0].replace('~~', '')
    variables = ','.join(variables)
    return variables.join(('Xor(', ')'))

def get_assignments(system):
    equations = system.split('\n')
    assignments = tuple(filter(lambda x: len(x) <= 16, equations))
    assignments = tuple(filter(lambda x: 'Z' not in x, assignments))
    equations = tuple(filter(lambda x: len(x) > 16 or 'Z' in x, equations))
    return '\n'.join(equations), assignments

def substitute(system, assignments):
    for assignment in assignments[::-1]:
        system = system.replace(assignment[0: 7], assignment[8:])
    system = system.replace('True', 'true')
    system = system.replace('False', 'false')
    system = system.replace('~~', '')
    return system

def simplify_in_place(system):
    equations = system.split('\n')
    evaluables = set(filter(lambda x: 'true' in x or 'false' in x, equations))
    xors = set(filter(lambda x: 'Xor' in x, evaluables))
    others = evaluables - xors
    for xor in xors:
        system = system.replace(xor[8:],\
                reduce_xor(xor[8:], r'~?[A-Za-z][0-9]{6}').replace(' ', ''))
    for other in others:
        system = system.replace(other[8:],\
                str(sympy.simplify_logic(other[8:])).replace(' ', ''))
    system = system.replace('False', 'false')
    system = system.replace('True', 'true')
    return system

def simplify_across(system):
    system = simplify_in_place(system)
    system, assignments = get_assignments(system)
    while len(assignments) != 0:
        system = substitute(system, assignments)
        system = simplify_in_place(system)
        system, assignments = get_assignments(system)
    return system

## reducing cnf

def to_total_cnf(system):
    equations = system.split('\n')
    cnf_form = [''] * len(equations)
    for i in range(len(equations)):
        reduced = equations[i].replace('=', ',')
        reduced = reduced.join(('Equivalent(', ')'))
        reduced = sympy.simplify_logic(reduced, 'cnf', True, True)
        reduced = str(reduced).replace(' ', '')
        reduced = reduced.replace('&', '\n')
        reduced = reduced.replace('(', '')
        reduced = reduced.replace(')', '')
        cnf_form[i] = reduced
    return '\n'.join(cnf_form)

def to_cnf(system):
    equations = system.split('\n')
    cnf_form = [''] * len(equations)
    for i in range(len(equations)):
        if 'Xor' in equations[i]:
            variables = re.findall(r'~?[A-Za-z][0-9]{6}', equations[i])
            variables[0] = '~' + variables[0]
            variables[0] = variables[0].replace('~~', '')
            variables = ','.join(variables)
            cnf_form[i] = variables.join(('Xor(', ')'))
        else:
            reduced = equations[i].replace('=', ',')
            reduced = reduced.join(('Equivalent(', ')'))
            reduced = sympy.simplify_logic(reduced, 'cnf', True, True)
            reduced = str(reduced).replace(' ', '')
            reduced = reduced.replace('&', '\n')
            reduced = reduced.replace('(', '')
            reduced = reduced.replace(')', '')
            cnf_form[i] = reduced
    return '\n'.join(cnf_form)

def cnf_get_assignments(system):
    clauses = system.split('\n')
    fixed_assignments = list(filter(lambda x: len(x) < 9, clauses))
    true_assignments = list(filter(lambda x: len(x) == 7, fixed_assignments))
    false_assignments = list(filter(lambda x: len(x) == 8, fixed_assignments))
    clauses = list(filter(lambda x: len(x) > 8, clauses))
    return '\n'.join(clauses), [true_assignments, false_assignments]

def cnf_substitute(system, assignments):
    for i in reversed(range(len(assignments[0]))):
        system = system.replace(assignments[0][i], "true")
    for i in reversed(range(len(assignments[1]))):
        system = system.replace(assignments[1][i][1:], "false")
    return system

def cnf_simplify_in_place(system):
    clauses = list(system.split('\n'))
    for i in range(len(clauses)):
        if ('true' in clauses[i]) or ('false' in clauses[i]):
            if 'Xor' in clauses[i]:
                clauses[i] = reduce_xor(clauses[i], r'~?[A-Za-z][0-9]{6}')
            else:
                clauses[i] = str(sympy.simplify_logic(\
                        clauses[i], 'cnf', True, True))
                clauses[i] = clauses[i].replace('&', '\n')
                clauses[i] = clauses[i].replace('(', '')
                clauses[i] = clauses[i].replace(')', '')
                clauses[i] = clauses[i].replace(' ', '')
    clauses = list(filter(lambda x: len(x) > 4, clauses))
    system = '\n'.join(clauses)
    return system

def cnf_simplify_across(system):
    system = cnf_simplify_in_place(system)
    system, assignments = cnf_get_assignments(system)
    while len(assignments[0]) + len(assignments[1]) != 0:
        system = cnf_substitute(system, assignments)
        system = cnf_simplify_in_place(system)
        system, assignments = cnf_get_assignments(system)
    return system

## utility for attacks

def fix_bits(wl, system, preimage_length):
    '''
    Parameters
    ----------
    wl : int 
        word length in bits
    system : string
        the representation of equations or clauses system in which we
        want to fix some bits in order to mount an attack
    preimage_length : int
        the amount of free consecutives bits starting from 0
    Returns
    -------
    string
        the representation of system in which we have fixed last (512 -
        preimage_length) bits
    '''
    W = [''] * (wl * 16)
    bits = [''] * (wl * 16)
    for i in range(len(W)):
        W[i] = bit('W' + fi(0) + fi(i // wl), wl - (i % wl) - 1)
    system = system.replace(W[preimage_length], 'true')
    bits[preimage_length] = '1'
    for i in range(preimage_length + 1, 503):
        system = system.replace(W[i], 'false')
        bits[i] = '0'
    length = list(f'{preimage_length:09b}')
    for i in range(9):
        system = system.replace(W[503 + i], str(bool(eval(length[i]))).lower())
        bits[503 + i] = length[i]
    fixed = [bits[i] + W[i] for i in range(preimage_length, wl * 16)]
    return fixed, system

def fix_first_bits(wl, system, first_fixed):
    W = [''] * (wl * 16)
    bits = [''] * (wl * 16)
    for i in range(len(W)):
        W[i] = bit('W' + fi(0) + fi(i // wl), wl - (i % wl) - 1)
    for i in range(first_fixed):
        rand_bit = random.getrandbits(1)
        bits[i] = str(rand_bit)
        system = system.replace(W[i], str(bool(rand_bit)).lower())
    fixed = [bits[i] + W[i] for i in range(first_fixed)]
    return fixed, system

def fix_random_bits(wl, system, free_bits):
    W = [''] * (wl * 16)
    fixed = []
    for i in range(len(W)):
        W[i] = bit('W' + fi(0) + fi(i // wl), wl - (i % wl) - 1)
    positions_fixed = random.sample(range(0, 416), 416 - free_bits)
    for i in range(len(positions_fixed)):
        rand_bit = random.getrandbits(1)
        fixed += [str(rand_bit) + W[positions_fixed[i]]]
        system = system.replace(W[positions_fixed[i]],\
                str(bool(rand_bit)).lower())
    system = system.replace(W[416], 'true')
    fixed += ['1' + W[416]]
    for i in range(417, 503):
        system = system.replace(W[i], 'false')
        fixed += ['0' + W[i]]
    length = list(f'{416:09b}')
    for i in range(9):
        system = system.replace(W[503 + i], str(bool(eval(length[i]))).lower())
        fixed += [length[i] + W[503 + i]]
    return fixed, system

def fix_for_name(wl, system, chars):
    W = [''] * (wl * 16)
    bits = [''] * (wl * 16)
    fixed = []
    for i in range(len(W)):
        W[i] = bit('W' + fi(0) + fi(i // wl), wl - (i % wl) - 1)
    for i in range(chars):
        system = system.replace(W[8 * i], 'false')
        bits[8 * i] = '0'
        fixed += [bits[8 * i] + W[8 * i]]
        system = system.replace(W[8 * i + 1], 'true')
        bits[8 * i + 1] = '1'
        fixed += [bits[8 * i + 1] + W[8 * i + 1]]
    system = system.replace(W[8 * chars], 'true')
    bits[8 * chars] = '1'
    fixed += [bits[8 * chars] + W[8 * chars]]
    for i in range(8 * chars + 1, 503):
        system = system.replace(W[i], 'false')
        bits[i] = '0'
    length = list(f'{8 * chars:09b}')
    for i in range(9):
        system = system.replace(W[503 + i], str(bool(eval(length[i]))).lower())
        bits[503 + i] = length[i]
    fixed += [bits[i] + W[i] for i in range(8 * chars + 1, wl * 16)]
    return fixed, system

