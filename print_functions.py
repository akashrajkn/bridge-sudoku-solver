#!/bin/python
from math import sqrt
from xmath import to_index
import re


def base10toN(num, n):
    """Change a  to a base-n number.
    Up to base-36 is supported without special notation."""
    num_rep={10:'a',
         11:'b',
         12:'c',
         13:'d',
         14:'e',
         15:'f',
         16:'g',
         17:'h',
         18:'i',
         19:'j',
         20:'k',
         21:'l',
         22:'m',
         23:'n',
         24:'o',
         25:'p',
         26:'q',
         27:'r',
         28:'s',
         29:'t',
         30:'u',
         31:'v',
         32:'w',
         33:'x',
         34:'y',
         35:'z'}
    new_num_string=''
    current= int(num)
    if num == 0:
        return "0"
    while current != 0:
        remainder = current % n
        if 36 > remainder > 9:
            remainder_string = num_rep[remainder]
        elif remainder >= 36:
            remainder_string = '(' + str(remainder) + ')'
        else:
            remainder_string = str(remainder)
        new_num_string = remainder_string + new_num_string
        current = int(current / n)
    return new_num_string

def print_board(b):
    width = int(sqrt(len(b)))
    height = width
    sub_width = int(sqrt(width))
    print (sub_width)
    if (width * height != len(b)):
        print ("Error! Invalid Board")
    for y in range(0, height):
        if y % sub_width == 0 and y > 0:
            print ()
            for x in range(0, width * 2):
                if (x/2) % sub_width == 0 and x > 0:
                    print ("-+", end = "")
                else:
                    print ("-", end="")
        print ("\n", end="")
        for x in range(0, width):
            if x % sub_width == 0 and x > 0:
                print ("| ", end = "")
            print (b[to_index(x, y, width)], end=" ")

def output_board(b):
    width = int(sqrt(len(b)))
    height = width
    ret_str = ""
    if (width * height != len(b)):
        print ("Error! Invalid Board")
        return ""
    for y in range(0, height):
        for x in range(0, width):
            ret_str += b[to_index(x, y, width)] + " "
        ret_str += "\n"
    return ret_str


def convert_board(b_original):
    b_original = b_original.replace("\n", "") # Do the cleaning thing
    b_original = b_original.replace("\t", "")
    b_original = b_original.replace(" ", "")
    b_original = re.sub(" \n", "", b_original)
    b_original = re.sub("[^0-9a-zA-Z]", "0", b_original)
    ret_list = []
    for char in b_original:
        ret_list.append(int(char, 36))
    return ret_list

if __name__ == "__main__":
    b = "e4...a.....519d8\
        .2.....b.dec..5.\
        .8..76....b...3c\
        .9.a...87..3..f.\
        9...e...37fd.c.1\
        ...f...a.e5..d..\
        ...c...fa.....7.\
        d7b....9..c..4.0\
        ..84d9.c....ab.3\
        ...9.5.768......\
        ..d...4..a......\
        ..f26.b0......e.\
        .e.7c35..4.1d..6\
        .fa.....2.6..1..\
        .......6....0e8f\
        8.c6a..........9"
    print_board(convert_board(b))
