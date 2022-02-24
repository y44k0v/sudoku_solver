# 9x9 puzzle
puzzle = [5, 3, 0, 0, 7, 0, 0, 0, 0,
          6, 0, 0, 1, 9, 5, 0, 0, 0,
          0, 9, 8, 0, 0, 0, 0, 6, 0,
          8, 0, 0, 0, 6, 0, 0, 0, 3,
          4, 0, 0, 8, 0, 3, 0, 0, 1,
          7, 0, 0, 0, 2, 0, 0, 0, 6,
          0, 6, 0, 0, 0, 0, 2, 8, 0,
          0, 0, 0, 4, 1, 9, 0, 0, 5,
          0, 0, 0, 0, 8, 0, 0, 7, 9]

      
# retrieve rows
def extract_rows(puzzle):
    rows = []
    row = []
    for i in puzzle:
        row.append(i)
        if len(row) == 9:
            rows.append(row)
            row = []
    return rows
    
      
# retrieving values in columns     
def extract_cols(puzzle):
  cols = []
  for i in range(9):
    col = []
    for j in range(9):
      col.append(puzzle[j][i])
    cols.append(col)

  return cols


  
# Retrieves values of every sqaure 3x3 cells
# the formula j//3+(i//3)*3 calculates the value of the 3x3 grid from 0 to 8 
# depending on the column j and row i, starting top left and ending bottom right 
def get_squares(puzzle):
  sqs = [[], [], [], [], [], [], [], [], []]
  for i in range(9):
    for j in range(9):
      sqs[j//3+(i//3)*3].append(puzzle[i][j])
  return sqs



# finds locations of missing values by 3x3 square, row and column
def find_all_empty(puzzle):
  locs = {}
  for row in range(9):
    for col in range(9):
      if puzzle[row][col] == 0:
        # cell(square), row and column numbers
        locs[(col//3+(row//3)*3),row, col] = []
  
  return locs  

# missing values per Square of 3 x 3
def missing_valuesSQs(SQs):
    missSQs =[]
    allrow = [x for x in range(1,10)]
    for i in range(9):
        row = []
        for j in allrow:
            if j not in SQs[i]:
                row.append(j)
        missSQs.append(row)
    return missSQs
    
# Assign all possible values to each value missing:
# acording to missign numbers from 1-9 in 3x3 squares, rows and columns

def possible_values(empty_info, SQs, Rows, Cols, missSQs):
    empty = empty_info
    for key in empty.keys():
        for val in missSQs[key[0]]:
            if val not in SQs[key[0]] and val not in Rows[key[1]] and val not in Cols[key[2]]:
                empty[key].append(val) 
    return empty

# cells that have numbers with only one possible value are filled and 
# missing numbers in 3x3 square are updated 
def assign_single(puzzle, empty, missSQs):
    p1 = puzzle
    missSQs = missSQs
    for k in empty.keys():
        if len(empty[k]) == 1:
            #print(k, empty[k])
            p1[k[1]][k[2]] = empty[k][0]
            missSQs[k[0]].pop(missSQs[k[0]].index(empty[k][0]))
        

    return p1,  missSQs

def print_sudoku(sudoku):
    for row in sudoku:
        print(row)
    

# Solution


def solution(puzzle):
    Rows = extract_rows(puzzle)
    Cols = extract_cols(Rows)
    SQs = get_squares(Rows)
    missing = find_all_empty(Rows) 
    total_missing = len(missing)
    missSQs = missing_valuesSQs(SQs)
    possible_numbers = possible_values(missing, SQs, Rows, Cols, missSQs)

    print_sudoku(Rows)
    print("\n")
    counter = 0      

    #initial solution
    solution,  missSQs = assign_single(Rows, possible_numbers, missSQs)
    

    while len(possible_numbers) > 0:
        Rows = solution
        Cols = extract_cols(solution)
        SQs = get_squares(solution)
        missing = find_all_empty(solution) 
        left_missing = len(missing)
        possible_numbers = possible_values(missing, SQs, Rows, Cols, missSQs)
        counter += 1
        solution,  missSQs = assign_single(solution, possible_numbers, missSQs)
        print("iteration: ",counter, "\t",round(100 - left_missing*100/total_missing, 2), "% solved")
    
    print("\n")
    return solution


print_sudoku(solution(puzzle))

