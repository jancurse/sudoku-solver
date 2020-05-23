import numpy as np
from sudoku import sudoku

board = np.load('./test-sudokus/evil2.npy')
my_sudoku = sudoku(board=board)
my_sudoku.solve()
print('Filled board:')
my_sudoku.print_board()
