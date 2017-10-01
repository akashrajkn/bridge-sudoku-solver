# Returns an integer index
def to_base(i, j, k, base, sudoku_num):
    if sudoku_num is 1:
        return base*base * (int(i) - 1) + base * (int(j) - 1) + (int(k) - 1) + 1

    return 729 + base*base * (int(i) - 1) + base * (int(j) - 1) + (int(k) - 1) + 1

# Returns a 3 tuple (i, j, k)
def from_base(n, base):
    sudoku_num = 1
    if abs(int(n)) > 729:
        sudoku_num = 2
        if int(n) < 0:
            n = int(n) + 729
        else:
            n = int(n) - 729

    n = int(n) - 1
    k = n % base + 1
    j = int(((n - (k - 1)) / base) % base + 1)
    i = int(((n - (k - 1)) - base * (j - 1))/ (base * base)) + 1
    return (i, j, k, sudoku_num)

#converts 2D coordinates to an index in a string
def to_index(i, j, base, sudoku_num):
    if sudoku_num is 1:
        return int(i) + int(base) * int(j)

    return 81 + int(i) + int(base) * int(j)
