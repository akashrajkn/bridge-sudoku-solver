# bridge-sudoku-solver
Solver for a MxN bridge sudoku

Steps for running -

1. To generate solved bridge - sudokus, run generator.py (which generates about 1000 sudokus for each overlap_m and overlap_n). The solved sudokus are located in datasets/ folder

2. To create bridge sudoku problems, run create-sudoku.py (Allows specification of how much area of the bridge-sudoku should be filled with givens). The problems are located in problems/ folder

3. analysis.py uses the minisat executable and creates output statistics.
