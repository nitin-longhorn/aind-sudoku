from utils import *

assignments = []

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
    for box in boxes:
        if len(values[box]) == 2:
            if values[box] in pair_map:
                pair_map[values[box]].append(box)
            else:
                pair_map[values[box]] = [box]


    for key in pair_map:

        if len(pair_map[key]) >= 2:
            naked_twin_map[key] = pair_map[key]

    for key, value in naked_twin_map.items():
        for v in value:
            row_item = [row for row in row_unit if v in row]
            col_item = [col for col in col_unit if v in col]
            sq_item = [sq for sq in square_unit if v in sq]

            if row_item[0]:
                for cell in row_item[0]:
                    if cell != v and values[cell] == key:
                        digits = list(key)
                        for cell in row_item[0]:
                            if cell not in value:
                                values[cell] = values[cell].replace(digits[0], "")
                                values[cell] = values[cell].replace(digits[1], "")

            if col_item[0]:
                for cell in col_item[0]:
                    if cell != v and values[cell] == key:
                        digits = list(key)
                        #print (digits)
                        for cell in col_item[0]:
                            if cell not in value:
                                values[cell] = values[cell].replace(digits[0], "")
                                values[cell] = values[cell].replace(digits[1], "")

            if sq_item[0]:
                for cell in sq_item[0]:
                    if cell != v and values[cell] == key:
                        digits = list(key)
                        #print (digits)
                        for cell in sq_item[0]:
                            if cell not in value:
                                values[cell] = values[cell].replace(digits[0], "")
                                values[cell] = values[cell].replace(digits[1], "")

    return values

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
    """
    If a box has a single value assigned, then none of the peers of this box can have this value.
    :param values:
        The dictionary of the sudoku

    :return values:
        The values dictionary with the values eliminated

    """
    values = naked_twins(values)
    solved_values = [b for b in boxes if len(values[b]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')

    return values

def only_choice(values):
    """
        If there is only one box in a unit which would allow a certain digit,
        then that box must be assigned that digit.

    :param values:
            The dictionary of the sudoku

    :return values:
        The values dictionary with values after applying the only choice constraint

    """
    nums = '123456789'
    for unit in unit_list:
        for digit in nums:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Combining functions eliminate and only choice to keep reducing and
    simplifying the sudoku until no more reduction is possible

    :param values:
        The dictionary of the sudoku that needs reduction

    :return values:
        The sudoku dictionary after reduction after applying eliminate and only choice
    """
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

        if (before_solved_number == after_solved_number):
            stalled = True
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
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
    temp_values = grid_values(grid)
    result = eliminate(temp_values)
    result2 = only_choice(result)
    result3 = reduce_puzzle(result2)
    result4 = search(result3)

    return result4

if __name__ == '__main__':
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
