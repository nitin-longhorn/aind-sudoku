from utils import *

assignments = []

<<<<<<< HEAD
# def assign_value(values, box, value):
#     """
#     Please use this function to update your values dictionary!
#     Assigns a value to a given box. If it updates the board record it.
#     """
#     values[box] = value
#     if len(value) == 1:
#         assignments.append(values.copy())
#     return values
=======
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
>>>>>>> origin/master

def naked_twins(values):

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    naked_twin_map = {}
    pair_map = {}
    display(values)
    print ( '\n\n*****************N1***********************\n\n')
    for box in boxes:
        if len(values[box]) == 2:
            if values[box] in pair_map:
                pair_map[values[box]].append(box)
            else:
                pair_map[values[box]] = [box]
    print ('Pair map: ', pair_map)


    for key in pair_map:
        # print ('here1')
        # print ('Key, Value: ', key, pair_map[key])
        if len(pair_map[key]) >= 2:
            naked_twin_map[key] = pair_map[key]
            # print ('here3: ', pair_map[key])
            # for unit in unit_list:
            #     # print ('here4')
            #     count = 0
            #     naked_boxes = []
            #     for val in pair_map[key]:
            #         # print ('here5')
            #         # print ('Unit and Val')
            #         #print (unit, val)
            #         if val in unit:
            #             naked_boxes.append(val)
            #             count = count + 1
            #             # print ('Here 6')
            #     if count >= 2:
            #         naked_twin_map[key] = naked_boxes

    print('Naked Twin Map: ', naked_twin_map)

    for key, value in naked_twin_map.items():
        for v in value:
            row_item = [row for row in row_unit if v in row]
            col_item = [col for col in col_unit if v in col]
            sq_item = [sq for sq in square_unit if v in sq]

            #print ('Row Item: ', row_item)
            #print ('Col Item: ', col_item)
            #print ('Sq Item: ', sq_item)

            if row_item[0]:
                print ('optimizing this row', row_item[0], 'for', v, 'values is ', value)
                for cell in row_item[0]:
                    if cell != v and values[cell] == key:
                        digits = list(key)
                        print (digits)
                        for cell in row_item[0]:
                            if cell not in value:
                                values[cell] = values[cell].replace(digits[0], "")
                                values[cell] = values[cell].replace(digits[1], "")

            display(values)
            print ('*****************N2***********************\n\n')

            if col_item[0]:
                print ('optimizing this col', col_item[0])
                for cell in col_item[0]:
                    if cell != v and values[cell] == key:
                        digits = list(key)
                        print (digits)
                        for cell in col_item[0]:
                            if cell not in value:
                                values[cell] = values[cell].replace(digits[0], "")
                                values[cell] = values[cell].replace(digits[1], "")
            display(values)
            print ('*****************N3***********************\n\n')

            if sq_item[0]:
                print ('optimizing this sq', sq_item[0])
                for cell in sq_item[0]:
                    if cell != v and values[cell] == key:
                        digits = list(key)
                        print (digits)
                        for cell in sq_item[0]:
                            if cell not in value:
                                values[cell] = values[cell].replace(digits[0], "")
                                values[cell] = values[cell].replace(digits[1], "")

    display(values)
    print ('*****************N6***********************\n\n')
    return values

    # for unit in unit_list:
    #     for box in unit:
    #         if len(values[box]) == 2:
    #             if naked_twin_map[values[box]]:
    #                 naked_boxes = [box, naked_twin_map[values[box]]]
    #             else:
    #                 naked_twin_map[values[box]] = box


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81


    all_values = '123456789'
    new_values = dict(zip(boxes, grid))
    for k in new_values.keys():
        if new_values[k] == '.':
            new_values[k] = all_values
    return new_values


def eliminate(values):
    values = naked_twins(values)
    solved_values = [b for b in boxes if len(values[b]) == 1]
    # print ('Solved Values', solved_values)
    for box in solved_values:
        digit = values[box]
        # print ('Box & Peers:', box, peers[box])
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    display(values)
    print ('*****************1.6***********************\n\n')
    #values = naked_twins(values)
    # display(values)
    # print ('*****************1.7***********************\n\n')
    return values

def only_choice(values):
    nums = '123456789'
    #print (unit_list)
    for unit in unit_list:
        for digit in nums:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        before_solved_number = 0
        after_solved_number = 0

        for box in boxes:
            if (len(values[box]) == 1):
                before_solved_number = before_solved_number + 1

        values = eliminate(values)
        values = only_choice(values)

        for box in boxes:
            if (len(values[box]) == 1):
                after_solved_number = after_solved_number + 1
        # print ("Here", before_solved_number, after_solved_number)

        if (before_solved_number == after_solved_number):
            # print ("Here", before_solved_number, after_solved_number)
            stalled = True
        if len([box for box in values.keys() if len(values[box]) == 0]):
            # print ('Here 2!!!!!!!!')
            return False
    return values

def search(values):


    print ("Counting")

    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # print (count)
    # count = count + 1

    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt




def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    temp_values = grid_values(grid)
    display(temp_values)
    print ('*****************1***********************\n\n')
    result = eliminate(temp_values)
    display(result)
    print ('*****************2***********************\n\n')
    result2 = only_choice(result)
    display(result2)
    result3 = reduce_puzzle(result2)
    print ('*****************3***********************\n\n')
    display(result3)
    result4 = search(result3)
    print ('*****************4***********************\n\n')
    display(result4)
    return result4
    display(solve(diag_sudoku_grid))


if __name__ == '__main__':

    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # temp_values = grid_values(diag_sudoku_grid)
    # display(temp_values)
    # print ('*****************1***********************\n\n')
    # naked_test_values = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
    #                         'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
    #                         'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
    #                         'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
    #                         'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
    #                         'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
    #                         'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
    #                         'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
    #                         'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
    #                         'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
    #                         'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
    # display(naked_test_values)
    # print ('*****************1.5***********************\n\n')
    # result = eliminate(naked_test_values)
    # display(result)
    # print ('*****************2***********************\n\n')
    # result2 = only_choice(result)
    # display(result2)
    # result3 = reduce_puzzle(result2)
    # print ('*****************3***********************\n\n')
    # display(result3)
    # result4 = search(result3)
    # print ('*****************4***********************\n\n')
    # display(result4)
    # #return result4
    # # display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
