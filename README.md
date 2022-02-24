# sudoku_solver

Basic sudoku solver that fills values where only one value option is available

Puzzle taken from the [wikipedia](https://en.wikipedia.org/wiki/Sudoku)  article.

|    |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |
|---:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
|  0 |   5 |   3 |   0 |   0 |   7 |   0 |   0 |   0 |   0 |
|  1 |   6 |   0 |   0 |   1 |   9 |   5 |   0 |   0 |   0 |
|  2 |   0 |   9 |   8 |   0 |   0 |   0 |   0 |   6 |   0 |
|  3 |   8 |   0 |   0 |   0 |   6 |   0 |   0 |   0 |   3 |
|  4 |   4 |   0 |   0 |   8 |   0 |   3 |   0 |   0 |   1 |
|  5 |   7 |   0 |   0 |   0 |   2 |   0 |   0 |   0 |   6 |
|  6 |   0 |   6 |   0 |   0 |   0 |   0 |   2 |   8 |   0 |
|  7 |   0 |   0 |   0 |   4 |   1 |   9 |   0 |   0 |   5 |
|  8 |   0 |   0 |   0 |   0 |   8 |   0 |   0 |   7 |   9 |


![puzzle](https://upload.wikimedia.org/wikipedia/commons/e/e0/Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg)


The input is in the form of a list of 81 elements with missing values represented by zeros:

```
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
```

Rows, columns and 3x3 grids (squares) are extracted:

```
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
  
```

A dictionary is created with the position of every missing value according with the tuple (square, row, column). Missing numbers per square are found and every possibble number is assigned to the missing values. Folowinf sudoku rules: only one value from 1-9 in every 3x3 square, row and column:

```
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
    
```

Cells with only one posibble valu from 1-9 are filled, and missing values for squares are updated accordingly:

```
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
    
```

The assignment of sigle values continues until puzzle is solved:

```
iteration:  1    7.84 % solved
iteration:  2    17.65 % solved
iteration:  3    31.37 % solved
iteration:  4    43.14 % solved
iteration:  5    52.94 % solved
iteration:  6    58.82 % solved
iteration:  7    62.75 % solved
iteration:  8    76.47 % solved
iteration:  9    96.08 % solved
iteration:  10   100.0 % solved

```

|    |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |
|---:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
|  0 |   5 |   3 |   4 |   6 |   7 |   8 |   9 |   1 |   2 |
|  1 |   6 |   7 |   2 |   1 |   9 |   5 |   3 |   4 |   8 |
|  2 |   1 |   9 |   8 |   3 |   4 |   2 |   5 |   6 |   7 |
|  3 |   8 |   5 |   9 |   7 |   6 |   1 |   4 |   2 |   3 |
|  4 |   4 |   2 |   6 |   8 |   5 |   3 |   7 |   9 |   1 |
|  5 |   7 |   1 |   3 |   9 |   2 |   4 |   8 |   5 |   6 |
|  6 |   9 |   6 |   1 |   5 |   3 |   7 |   2 |   8 |   4 |
|  7 |   2 |   8 |   7 |   4 |   1 |   9 |   6 |   3 |   5 |
|  8 |   3 |   4 |   5 |   2 |   8 |   6 |   1 |   7 |   9 |

![solution](https://upload.wikimedia.org/wikipedia/commons/1/12/Sudoku_Puzzle_by_L2G-20050714_solution_standardized_layout.svg)


Does not do good on very hard puzzles like the one below, extra implementations needed for the cases where missing values have not  a single value as an option anymore. It will do well on easy, averages and hard puzzles. Test to be implemented

```

[0, 0, 6, 0, 5, 0, 0, 3, 0]
[3, 0, 0, 7, 6, 0, 4, 0, 0]
[0, 8, 0, 0, 0, 0, 0, 0, 2]
[0, 0, 0, 0, 0, 0, 0, 2, 0]
[4, 1, 0, 0, 2, 0, 0, 7, 5]
[0, 9, 0, 0, 0, 0, 0, 0, 0]
[6, 0, 0, 0, 0, 0, 0, 8, 0]
[0, 0, 8, 0, 4, 1, 0, 0, 9]
[0, 2, 0, 0, 3, 0, 5, 0, 0]

```


