Software developed and provided by Alessandro De Piccoli

RESEARCH AND DEVELOPMENT AGREEMENT: University of Milan and Technology Innovation Institute of Abu Dhabi

Research project: "Algebraic analysis of HMAC-SHA-1"

Main supervisors/point of contacts: Andrea Visconti (University of Milan), Emanuele Bellini (Technology Innovation Institute of Abu Dhabi)

# Shanatomy

Software requested to completely enjoy *Shanatomy*:

0. [Python3](https://www.python.org/) (in `/usr/lib/python3` by default, if it has a different path, change accordingly `Makefile`);
1. [Sympy](https://www.sympy.org/en/index.html), a Python module to perform algebraic manipulations;
2. [CryptoMiniSat](https://github.com/msoos/cryptominisat), a SAT solver with
   xor extension or any other SAT solver able to output model in DIMACS
standard;

Before venturing into the code, it is suggested to read this guide without skipping parts.

## A bit of documentation (optional)

In order to make clear how the software is designed, there are docstrings for
some functions in the main module, `bitpy.py`. You can build the documentation
by simply run the following command.

> `pydoc3 -w bitpy`

This will generate a file called `bitpy.html` from which you can understand the
background philosophy of *Shanatomy*.

## Building the system

Once being in the Shanatomy directory, type

> `make`

to have the correct tree and, additionally, a basic test to prove that the
system generated is a correct SHA-1. If all is ok, type

> `make finalize`

to have the complete setup to mount a preimage attack.

## Mount a preimage attack to SHA-1

*Remark*: consider that the implemented attack uses a digest coming from strings, so, it is a second preimage attack. But, if we are given only a SHA-1 digest without knowing the input, second preimage attack is equivalent to a first preimage attack from an implementation point of view.

Go in *Shanatomy* directory.

0. > `python3 map_attacker.py 32 19 000 440 <file>`

\<file\> is either `structures/sha_1_cnf.txt` or
`structures/sha_1_total_cnf.txt`. Please note that the former will produce a
CNF form with XOR extension for CryptoMiniSat solver, the latter a CNF form of
SHA-1 totally compliant to DIMACS standard. The arguments mean that you want to
attack a 32-bit SHA-1, round 19 of message 000 (set by default to `Chiara`),
using 440 bits free. 

You're ready to run

1. > `time cryptominisat5 --verb 0 temp/to_solve_000.cnf >
temp/preimage_000.txt`

or changing `cryptominisat5` with your favourite SAT solver. If the solver can
generate a model and this is compliant to the DIMACS standard, check whether
`temp/preimage_000.txt` contains lines starting with `v`. If so, you can go on.

You can now run 

2. > `python3 map_from_sat.py 32 000`

in order to write the preimage found by the SAT solver in the compliant format
for *Shanatomy*.

By running

3. > `python3 map_designer.py 32 1 ./temp/preimage_000.txt 001`

the map files are obtained and are assigned id `001` (check `maps` directory).

You can now check the correctness of the preimage by checking the digest at
round 19 using following commands

4. > `sed -ne 20p maps/states_000.txt`
5. > `sed -ne 20p maps/states_001.txt`

and seeing the correct match. Moreover, you can open the `maps/block_001.txt`
to see the pre-image found by the SAT solver.

## Mount a preimage attack to a *chosen* string

You have just to generate the maps for the chosen string. Say that you want to
attack `Elena` string. Run

> `python3 map_designer.py 32 0 Elena 010`

and this will create `maps/states_010.txt`, the indispensable file to mount the
attack. Now go back to the point 0 of previous section and replace each
occurence of `000` with `010`. In general, the recommended format for id of
maps is three digits, i.e., `[0-9]{3}`.

**Pay attention**, do not overwrite maps files if you want to see the match.
Especially in point 3 of the previous section the last system argument has to
be different from the one used in attack.

## More blocks

SHA-1 could perform its computation over many blocks and, in this perspective
it could be run the following command.

> `python3 sha_1_n_blocks.py 32 2`

It will print a request for test. Please note that they are allowed only 2
chars: `y` or `n`, any other char will prompt an error message. By choosing
`n`, the process will exit saving in a file the SHA-1 system on multiple
blocks. By choosing `y`, you will have to enter a string compliant to the
specifications printed. If it is all ok, it will be printed the SHA-1 digest of
your string.

## HMAC-SHA-1

*Shanatomy* can also construct the general system for HMAC-SHA-1. It's only an
experimental feature, but it could be checked that 

> `python3 hmac_sha_1_generator.py 32 Chiara Ingegnere`

and

> `echo -n "Chiara" | openssl dgst -sha1 -hmac "Ingegnere"`

return the same output. "Chiara" is the value and "Ingegnere" is the key. They
can be changed, but please note that the code can only support values no longer
than 55 chars and keys no longer than 64 chars (i.e. 512 bits).

## Statistics

In order to give some informations about boolean or algebraic systems (see
below **SHA-1 over GF(2)**), it has been written the `statistic.py` module. You
have to give its one system argument, i.e., the path of the file you want to
analyze. If you have read and followed all the guide, you have now, e.g.,
`structures/sha_1_cnf.txt` or `structures/sha_1_total_cnf.txt` and you can test
them. For example, try to type following command.

> `python3 statistics.py structures/sha_1_total_cnf.txt`

## SHA-1 over GF(2)

It is well known that we can represent SHA-1 as a system of equation over
GF(2). For this purpose, we have tailored an handmade system for SHA-1, you can
find it in the file `sha_1_gf2.txt`. It is projected just for one block
message. You can test it to verify that it is the correct SHA-1 system by
running

> `python3 gf2_tester.py sha_1_gf2.txt Chiara`

and obtain the SHA-1 digest to check with your favourite SHA-1 calculator.
Replace 'Chiara' with the string you want to test.

Beside this we have some scripts.

0. `gf2_00_separator.py` can definitely separate the quadratic part of SHA-1
   system by introducing new variables. Returned system will be stored in
`structures/gf2` directory.
1. `gf2_01_cutter.py` can cut the separated system in clever way, obtaining
   just first `x` round. Give the desired number of rounds as a system
argument.
2. `gf2_02_translator.py` can translate the representation over GF(2) in the
   *Shanatomy* standard.

