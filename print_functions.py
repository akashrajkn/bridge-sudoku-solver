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


def output_board(b):
    width = int(sqrt(len(b)/2))
    height = width
    ret_str = ""
    if (width * height *2 != len(b)):
        print ("Error! Invalid Board")
        return ""
    for y in range(0, height):
        for x in range(0, width):
            ret_str += b[to_index(x, y, width, 1)] + " "
        ret_str += "\n"

    ret_str += "\n"
    for y in range(0, height):
        for x in range(0, width):
            ret_str += b[to_index(x, y, width, 2)] + " "
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
