"""Killer sudoku encoder

    Usage:
        ks [input_file name]

    * The output text is in Yices Language.

"""
import sys

# =========
# CONSTANTS
# =========
__author__ = 'Viet Vu'
__email__ = 'vietvudanh@gmail.com'
__version__ = '0.2'
__description__ = """
    ks ver3, beta.
    trying to separate assert command, not use one assert command
    add constrain for cells to be smaller or equal than 9
    => seems much better"""

BLOCK_SIZE = 3  # Block size that we using in the input
# actually, it isn't considered yet

# help text in case there is no input
HELP_TEXT = """Killer sudoku encoder

    Usage:
        ks [input_file name]

    * The output text is in Yices Language."""


def encode(input):
    """Encode the formatted Killer Sudoku problem in to Yices language

    :param input string"""

    output = ''

    # define
    output += '; Define variables\n'
    for row in range(1, BLOCK_SIZE ** 2 + 1):
        for col in range(1, BLOCK_SIZE ** 2 + 1):
            output += '(define x' + str(row) + str(col) + ' :: int)\n'

    # constrain 0.1: numbers are greater than 0
    output += '\n; Numbers are greater than 0\n'
    for row in range(1, BLOCK_SIZE ** 2 + 1):
        for col in range(1, BLOCK_SIZE ** 2 + 1):
            output += '(assert(<= x' + str(row) + str(col) + ' 9))\n'

    # constrain 0.2: numbers are greater than 0
    output += '\n; Numbers are greater than 0\n'
    for row in range(1, BLOCK_SIZE ** 2 + 1):
        for col in range(1, BLOCK_SIZE ** 2 + 1):
            output += '(assert(> x' + str(row) + str(col) + ' 0))\n'

    # constrain 1: no duplicate in one row
    output += '\n; No duplicate cells in a row\n'
    for col in range(1, BLOCK_SIZE ** 2 + 1):
        output += '(assert(distinct '
        for row in range(1, BLOCK_SIZE ** 2 + 1):
            output += 'x' + str(row) + str(col) + ' '
        output += '))\n'

    # constrain 2: no duplicate in one col
    output += '\n; No duplicate cells in a column\n'
    for row in range(1, BLOCK_SIZE ** 2 + 1):
        output += '(assert(distinct '
        for col in range(1, BLOCK_SIZE ** 2 + 1):
            output += 'x' + str(row) + str(col) + ' '
        output += '))\n'

    # constrain 3: no duplicate in one block n*n
    output += '\n; No duplicate cells in a block\n'
    for i in range(0, BLOCK_SIZE):
        for j in range(0, BLOCK_SIZE):
            # seed is the first cell of each block
            seed_row = i * BLOCK_SIZE + 1
            seed_col = j * BLOCK_SIZE + 1

            output += '(assert(distinct '
            # log's cells are different
            for m in range(0, BLOCK_SIZE):
                for n in range(0, BLOCK_SIZE):
                    output += 'x' + str(seed_col + m) + str(seed_row + n) + ' '
            output += '))\n'

    # clean empty lines
    input = '\n'.join([line for line in input.split('\n') if line.strip() != ''])

    # constrain 4: No duplicate cells in a region
    constrain4 = ''
    # constrain 5: No sum of region is as defined
    constrain5 = ''

    constrain4 += '\n; No duplicate cells in region\n'
    lines = input.split('\n')
    for line in lines:
        constrain4 += '(assert(distinct '
        for x in [i for i in line.split(' ')[1:] if i.strip() != '']:  # clean empty white space
            constrain4 += 'x' + str(x) + ' '
        constrain4 += '))\n'

    constrain5 += '\n; Sum of region is defined\n'
    lines = input.split('\n')
    for line in lines:
        constrain5 += '(assert(= '
        constrain5 += line.split(' ')[0]
        constrain5 += ' (+ '
        for x in [i for i in line.split(' ')[1:] if i.strip() != '']:  # clean empty white space
            constrain5 += 'x' + str(x) + ' '
        constrain5 += ')))\n'

    output += constrain4
    output += constrain5

    # check
    output += '(check)\n'

    # show model
    output += '(show-model)\n'

    # show stats
    output += '(show-stats)'

    return output


if __name__ == '__main__':

    input_params = sys.argv

    # if there is no input, print help
    if len(input_params) < 2:
        print(HELP_TEXT)
    # else, take first argument and process
    # ignore the rest
    else:
        try:
            # read file
            content = open(input_params[1]).read()

            # encode and print
            encoded = encode(content)
            open('output.ys', 'w').write(encoded)

        except FileNotFoundError as e:
            print('File' + str(input_params[1]) + ' not found')
        except Exception as e:
            print(e)