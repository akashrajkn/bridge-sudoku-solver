import os
import random
from math import sqrt
from print_functions import convert_board, output_board, base10toN
from subprocess import Popen, PIPE
from xmath import to_base, from_base, to_index

import argparse
parser = argparse.ArgumentParser(description="Solve a bridge-sudoku puzzle")
parser.add_argument('minisatexe')
parser.add_argument('temp_file')
parser.add_argument('minisat_output')
args = parser.parse_args()
# print(args)

def get_dimacs_output(board, m, n):
    size = int(sqrt(len(board)/2))
    numbers = size

    variables = size * size * numbers * 2
    dimacs_output = ""
    clauses = 0

    # print ("Generating Board Requirements...")

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
    return dimacs_output


def call_minisat_for_data_generation(sudoku, m, n):
    dimacs_output = get_dimacs_output(sudoku, m, n)
    # Write to a temporary file

    temp_file = open(args.temp_file, 'w')
    temp_file.write(dimacs_output)
    temp_file.close()
    # print(args.minisat_output)
    # Call minisat
    try:
        # TODO: Add rnd-frq option for generating
        p = Popen([args.minisatexe, temp_file.name,
                   args.minisat_output], stdin=PIPE,
                   stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        # print('HASDHFHASDF')

        # args.outputfile.write(output)
    except OSError:
        print ("Fatal Error: Could not run ", '~/./minisat')
        exit(1)

    with open(args.minisat_output, "r") as f_in:
        solved_board = f_in.read()
        # print('solved_board')
        # print(solved_board)

    # Clean solved board
    solved_board = solved_board.split()
    if (solved_board[0] != "SAT"):
        # print ("Unsolvable puzzle")
        return 0, 'UNSAT'
    # Remove "SAT"
    solved_board.pop(0)

    # convert to string
    sb1 = ""
    sb2 = ""
    for s in solved_board:
        try:
            l = int(s)
            if l > 0:
                (i, j, k, sudoku_num) = from_base(l, 9)
                if sudoku_num == 1:
                    sb1 += base10toN(k, 36)
                else:
                    sb2 += base10toN(k, 36)
        except:
            pass

    # rebuild the solved board non-transpose
    fixed = ""
    for i in range(0, 9):
        for j in range(0, 9):
            fixed += sb1[to_index(i, j, 9, 1)]

    for i in range(0, 9):
        for j in range(0, 9):
            fixed += sb2[to_index(i, j, 9, 1)]

    return 1, fixed

# m is overlap row, n is overlap column, i is the number of iterations
for m in range(1, 10):
    for n in range(1, 10):
        print ('m = ' + str(m) + ' ; n = ' + str(n))
        folder_name = str(m) + 'x' + str(n)
        # Create folder if it doesn't exist
        # if not os.path.exists('datasets/' + folder_name):
        #     os.makedirs('datasets/' + folder_name)

        for i in range(1, 1001):
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            sudoku = ['0']*162
            # Fill 9 numbers in the first sudoku
            for j in range(0, 9):
                random.shuffle(numbers)
                num = numbers.pop()

                while True:
                    index = random.randint(0, 80)
                    if sudoku[index] == '0':
                        sudoku[index] = str(num)
                        break
                        # TODO: Add to second sudoku if it doesn't work.
            sudoku = ''.join(sudoku)

            solved, fixed = call_minisat_for_data_generation(sudoku, m, n)

            if solved:
                filename = 'datasets/' + folder_name + '/' + str(i) + '.txt'

                f = open(filename, 'w+')
                f.write(output_board(fixed))

            # print(sudoku, m, n)
            # print("\n")
            # initialize empty array
            # randomly choose row and column
            # if row + column in bridge area, add to second sudoku
            # Create first draft of the dataset
            # Number of total givens = total_area * 0.20987 - remove the remaining numbers
