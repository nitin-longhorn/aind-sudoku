rows = 'ABCDEFGHI'
cols = '123456789'


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return


def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_unit = [cross(r, cols) for r in rows]
col_unit = [cross(rows, c) for c in cols]
square_unit = [cross(s, t) for s in ['ABC', 'DEF', 'GHI'] for t in ['123', '456', '789']]
diagonal1 = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
diagonal2 = ['A9','B8','C7','D6','E5','F4','G3','H2','I1']
diagonal_list1 = [diagonal1 for row in row_unit]
diagonal_list2 = [diagonal2 for row in row_unit]

#unit_list = row_unit + col_unit + square_unit
unit_list = row_unit + col_unit + square_unit + diagonal_list1 + diagonal_list2
print (unit_list)
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)