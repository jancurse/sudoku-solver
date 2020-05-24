# Sudoku Solver

## Usage
'sudoku.py' implements a simple sudoku class.
  - `my_sudoku = sudoku(board)` creates a sudoku, where board is a 2d array of shape (9,9) representing the board
  - `my_sudoku.solve()` solves the sudoku
  - `my_sudoku.print_board()` prints the current board (if solve has been called, this is the solution)
  
'test_script.py' runs an example
 
'./test-sudokus' contains a few random sudokus of different difficulties from https://www.websudoku.com/ that can be easilly loaded with np.load()

## Algorithm
We maintain a number of candidate lists, which are attributes of the sudoku.
  - `self.candidates` contains for each field a list of all possible numbers
  - `self.row_candidates` contains for each number x and row i the possible positions of x
  - `self.col_candidates` and `self.squ_candidates` are similar
We first go through the board and remove all blocked candidates.
Then, whenever there is a unique candidate, we fill it in and update the candidates.
At some point, this will get stuck. Medium level sudokus are probably solved at this point.
If we are not done, we choose a field with few candidates, and try each of them and iterate.
