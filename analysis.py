#!/usr/bin/python3

from print_functions import convert_board, output_board, base10toN
from math import sqrt
from xmath import to_base, from_base, to_index
from subprocess import Popen, PIPE
from output_parser import parse_minisat_output

import argparse
parser = argparse.ArgumentParser(description="Solve a bridge-sudoku puzzle")
parser.add_argument('outputfile', type=argparse.FileType('a'))
parser.add_argument('minisatexe')
parser.add_argument('tmp_out')
parser.add_argument('tmp_in')
args = parser.parse_args()


def count_total_givens(sudoku):
    sudoku = sudoku.replace('\n', '')
    sudoku = sudoku.replace('\t', '')
    sudoku = sudoku.replace(' ', '')
    sudoku = list(sudoku)

    count = 0
    for num in sudoku:
        if num != '0':
            count += 1
    return count

for m in range(1, 10):
    for n in range(1, 10):
        folder_name = str(m) + 'x' + str(n)

        for iteration in range(1, 1001):
            filepath = 'problems/' + folder_name + '/' + str(iteration) + '.txt'

            try:
                with open(filepath, "r") as f_in:
                    sudoku = f_in.read()
                board = convert_board(sudoku)

                size = int(sqrt(len(board)/2))
                numbers = size

                variables = size * size * numbers * 2
                dimacs_output = ""
                clauses = 0

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

                for i in range(size - m + 1, size + 1):
                    for j in range(size - n + 1, size + 1):
                        for k in range(1, numbers + 1):
                            x = to_base(i, j, k, size, 1)
                            y = to_base(i - (size - m), j - (size - n), k, size, 2)
                            dimacs_output += "-{0} {1} 0\n".format(x, y)
                            dimacs_output += "{0} -{1} 0\n".format(x, y)
                            clauses += 2

                dimacs_output = "p cnf {0} {1}\n".format(variables, clauses) + dimacs_output

                # Write to file
                # , type=argparse.FileType('w')
                temp_file = open(args.tmp_out, 'w')
                temp_file.write(dimacs_output)
                temp_file.close()

                try:
                    # TODO: Add rnd-frq option for generating
                    p = Popen([args.minisatexe, args.tmp_out, args.tmp_in], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
                    rc = p.returncode

                    total_givens = count_total_givens(sudoku)

                    # TODO: total_givens, bridge_givens need to be sent
                    results = parse_minisat_output(output.decode("utf-8"), m, n, iteration, total_givens, 0)
                    result_keys = ['m', 'n',  'iteration', 'total_givens', 'bridge_givens', 'restarts',
                                   'conflicts', 'decisions', 'propagations', 'conflict_literals',
                                   'memory_used', 'cpu_time']

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

            except Exception as e:
                print (e)
                print('Exception occured at, m = {0}, n={1}, iteration={2}'.format(m, n, iteration))

args.outputfile.close()
