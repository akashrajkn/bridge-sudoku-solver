import os
import re
import random
from print_functions import output_board


for m in range(1, 10):
    for n in range(1, 10):

        overlap_region = {}
        idx = 0
        for m_temp in range(0, 9):
            for n_temp in range(0, 9):
                if m_temp >= (9 - m) and n_temp >= (9-n):
                    overlap_region[idx] = 161 - idx
                    overlap_region[161-idx] = idx
                idx += 1

        folder_name = str(m) + 'x' + str(n)

        for i in range(1, 1001):
            filepath = 'datasets/' + folder_name + '/' + str(i) + '.txt'
            try:
                with open(filepath, "r") as f_in:
                    sudoku = f_in.read()
                sudoku = sudoku.replace('\n', '')
                sudoku = sudoku.replace('\t', '')
                sudoku = sudoku.replace(' ', '')
                sudoku = list(sudoku)

                # print(sudoku)
                total_squares= 162 - m*n
                total_givens = int((162 - m*n)*21 / 100)

                indices = list(range(0, 161))

                for num in range(0, total_squares - total_givens):

                    random.shuffle(indices)
                    index = indices.pop()
                    sudoku[index] = 0
                    # FIXME: remove in overlap region
                    # if index in overlap_region.keys():
                    #     sudoku[overlap_region[index]] = 0

                    # TODO: Make this change
                    # if sudoku[index] == 0:
                    #     pass

                sudoku2 = [str(x) for x in sudoku]
                sudoku2 = ''.join(sudoku2)

                problem_file = 'problems/' + folder_name + '/' + str(i) + '.txt'

                f = open(problem_file, 'w+')
                f.write(output_board(sudoku2))

            except:
                print('Exception occured at, m = {0}, n={1}, i={2}'.format(m, n, i))
