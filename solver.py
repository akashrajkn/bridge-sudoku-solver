#!/usr/bin/python3

from print_functions import convert_board, output_board, base10toN
from math import sqrt
from xmath import to_base, from_base, to_index
from subprocess import Popen, PIPE
from output_parser import parse_minisat_output

import argparse
parser = argparse.ArgumentParser(description="Solve a bridge-sudoku puzzle")
parser.add_argument('inputfile', type=argparse.FileType('r'))
parser.add_argument('outputfile', type=argparse.FileType('a'))
parser.add_argument('minisatexe')
parser.add_argument('tmp_out', type=argparse.FileType('w'))
parser.add_argument('tmp_in')
args = parser.parse_args()

board = convert_board(args.inputfile.read())

# -----------------------------------------
# CONVERT TO DIMACS
# -----------------------------------------


size = int(sqrt(len(board)/2))
numbers = size
# FIXME: overlap m and n should be general, get from arguments
overlap_m = 3
overlap_n = 3

# The number of individual possibilities
variables = size * size * numbers * 2
dimacs_output = ""
clauses = 0

print ("Generating Board Requirements...")

for sudoku_num in [1, 2]:
    dimacs_output += "c the board requirements for {0}\n".format(sudoku_num)
    for j in range(0, size):
        for i in range(0, size):
            value = int(board[to_index(i, j, size, sudoku_num)])
            if value != 0:
                value = to_base(i + 1, j + 1, value, size, sudoku_num)
                clauses += 1
                dimacs_output += "{0} 0\n".format(value)

    dimacs_output += "c at least one number per entry for {0}\n".format(sudoku_num)
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            for k in range(1, numbers + 1):
                dimacs_output += "{0} ".format(to_base(i, j, k, size, sudoku_num))
            dimacs_output += "0\n"
            clauses += 1

    dimacs_output += "c Row constraint for {0}\n".format(sudoku_num)
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            for k in range(1, numbers + 1):
                for j_s in range(j + 1, numbers + 1):
                    dimacs_output += "-{0} -{1} 0\n".format(
                        to_base(i, j, k, size, sudoku_num), to_base(i, j_s, k, size, sudoku_num))
                    clauses += 1

    dimacs_output += "c Column constraint for {0}\n".format(sudoku_num)
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            for k in range(1, numbers + 1):
                for i_s in range(i + 1, numbers + 1):
                    dimacs_output += "-{0} -{1} 0\n".format(to_base(i, j, k, size, sudoku_num),
                                                            to_base(i_s, j, k, size, sudoku_num)
                                                            )
                    clauses += 1

    dimacs_output += "c 3x3 block constraint for {0}\n".format(sudoku_num)

    sq = int(sqrt(size))
    for k in range(1, size + 1):
        for a in range(sq):
            for b in range(sq):
                for u in range(1, sq+1):
                    for v in range(1, sq):
                        for w in range(v + 1, sq + 1):
                            dimacs_output += "-{0} -{1} 0\n".format(
                                to_base(sq*a + u, sq*b + v, k, size, sudoku_num),
                                to_base(sq*a + u, sq*b + w, k, size, sudoku_num))
                            clauses += 1
    for k in range(1, size + 1):
        for a in range(sq):
            for b in range(sq):
                for u in range(1, sq):
                    for v in range(1, sq+1):
                        for w in range(u + 1, sq+1):
                            for t in range(1, sq+1):
                                dimacs_output += "-{0} -{1} 0\n".format(
                                    to_base(sq*a+u, sq*b+v, k, size, sudoku_num),
                                    to_base(sq*a+w, sq*b+t, k, size, sudoku_num))
                                clauses += 1

# Constraint for bridge - overalapping area
dimacs_output += "c bridge area constraint\n"

for i in range(size - overlap_m + 1, size + 1):
    for j in range(size - overlap_n + 1, size + 1):
        for k in range(1, numbers + 1):
            x = to_base(i, j, k, size, 1)
            y = to_base(i - (size - overlap_m), j - (size - overlap_n), k, size, 2)
            dimacs_output += "-{0} {1} 0\n".format(x, y)
            dimacs_output += "{0} -{1} 0\n".format(x, y)
            clauses += 2

dimacs_output = "p cnf {0} {1}\n".format(variables, clauses) + dimacs_output

# Write to file
args.tmp_out.write(dimacs_output)
args.tmp_out.close()

print ("Board Requirements Generated")

# -----------------------------------------
# Run minisat
# -----------------------------------------
print ("Running SAT solver")
try:
    # TODO: Add rnd-frq option for generating
    p = Popen([args.minisatexe, args.tmp_out.name, args.tmp_in], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode

    # args.outputfile.write(output)

    # TODO: total_givens, bridge_givens need to be sent
    results = parse_minisat_output(output.decode("utf-8"), overlap_m, overlap_n, 0, 0)
    result_keys = ['m', 'n',  'total_givens', 'bridge_givens', 'restarts', 'conflicts',
                   'decisions', 'propagations', 'conflict_literals', 'memory_used',
                   'cpu_time']

    line = ''
    for k in result_keys:
        line += str(results[k])
        line += ','
    line = line[:-1]
    line += '\n'
    args.outputfile.write(line)


except OSError:
    print ("Fatal Error: Could not run", args.minisatexe)
    exit(1)

# -----------------------------------------
# Load solved board
# -----------------------------------------

with open(args.tmp_in, "r") as f_in:
    solved_board = f_in.read()

# -----------------------------------------
# CONVERT SOLVED BOARD
# -----------------------------------------

# Clean solved board
solved_board = solved_board.split()
if (solved_board[0] != "SAT"):
    print ("Unsolvable puzzle")
    exit(0)
# Remove "SAT"
solved_board.pop(0)

# # convert to string
# sb1 = ""
# sb2 = ""
# for s in solved_board:
#     try:
#         l = int(s)
#         if l > 0:
#             (i, j, k, sudoku_num) = from_base(l, size)
#             if sudoku_num == 1:
#                 sb1 += base10toN(k, 36)
#             else:
#                 sb2 += base10toN(k, 36)
#     except:
#         pass
#
# # rebuild the solved board non-transpose
# fixed = ""
# for i in range(0, size):
#     for j in range(0, size):
#         fixed += sb1[to_index(i, j, size, 1)]
#
# for i in range(0, size):
#     for j in range(0, size):
#         fixed += sb2[to_index(i, j, size, 1)]
#
# # args.outputfile.write(output_board(fixed))
