assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    #pass
    return [s+t for s in A for t in B]

# Function defined to reverse a string
#This function is later used to define the diagonal units
def reversed_string(a_string):
    return a_string[::-1]
def intersect(a, b):
    return list(set(a) & set(b))

boxes=cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units=[[a+b for a,b in zip(rows,cols)],[a+b for a,b in zip (rows,reversed_string(cols))] ]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
""

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #iterate over all units
    for unit in unitlist:
        #make a list of all unsolved boxes in the unit
        unsolved_boxes=[box for box in unit if len(values[box])>1 ]
        for box1 in unsolved_boxes:
            if len(values[box1])>2:
                continue
            for box2 in unsolved_boxes:
                if box1==box2:
                    continue
                if values[box1]==values[box2]:
                    for box3 in unsolved_boxes :
                        if box3==box1 or box3==box2:
                            continue
                        for digit in values[box1]:
                            #values[box3]=values[box3].replace(digit,'')
                            values = assign_value(values, box3, values[box3].replace(digit,''))
    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

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
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))
    #pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print (len(values))
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    #pass

def eliminate(values):
    for key in values:
        if len(values[key])==1:
            for k in peers[key]:
                #values[k] = values[k].replace(values[key], '')
                values=assign_value(values,k,values[k].replace(values[key],''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            x=list()
            for box in unit:
                if digit in values[box]:
                    x.append(box)
            #print(x)
            if len(x) == 1:
                #values[x[0]]=digit
                values=assign_value(values,x[0],digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
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
    puzzle=grid_values(grid)
    return search(puzzle)

##HELPER_DELETE_AFTERWARDS####
def my_grid_values(box,grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 9
    return dict(zip(box, values))
    #pass
######



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid2='..29.4..5....7.........3....9......1..........4.....2..6.........73....94.5...2..'
    display(solve(diag_sudoku_grid))
    ##naked_twin_try#############
    letters='A'
    digits='123456789'
    sudoku_values='468...15.'
    box=cross(letters,digits)
    puzzle=my_grid_values(box,sudoku_values)
    puzzle['A4']='2379'
    puzzle['A8']='2379'
    puzzle['A5']='379'
    puzzle['A6']='23'
    puzzle['A9']='23'
    #print(puzzle)
    #y=list()
    ######################################3
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
