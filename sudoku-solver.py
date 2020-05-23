import numpy as np

def find_block(i, j):
    """
    :return: all coordinates of fields in the same block as (i,j)
    """
    I, J = int(i / 3), int(j / 3)
    block = []
    for ii in range(3):
        for jj in range(3):
            block.append((3 * I + ii, 3 * J + jj))
    return block

def to_small_square(i,j):
    """
    :return: Given coordinate (i,j) of a field, returns (ii,jj), where
    (i,j) is the jj-th number in the ii-th small square counting in lexicographic order
    """
    I, J = int(i / 3), int(j / 3)
    ii = 3*I+J
    jj = 3*(i - 3*I)+(j-3*J)
    return ii, jj

def to_big_square(ii,jj):
    """
    :return: Gives coordinates (i,j) of the jj-th field in the ii-th small square
    """
    I, II = int(ii/3), int(jj/3)
    J, JJ = ii % 3, int(jj % 3)

    i = 3*I + II
    j = 3*J + JJ
    return i, j

class sudoku:

    def __init__(self, board=np.zeros((9,9))):
        self.board = np.array(board)
        self.candidates = [[list(range(1,10)) for i in range(9)] for j in range(9)]
        # for i in range(9):
        #     for j in range(9):
        #         if board[i,j]:
        #             self.candidates[i][j]=[board[i,j]]

        self.row_candidates = [[list(range(9)) for i in range(9)] for x in range(10)]
        self.col_candidates = [[list(range(9)) for j in range(9)] for x in range(10)]
        self.squ_candidates = [[list(range(9)) for j in range(9)] for x in range(10)]

        self.empty_fields = [(i,j) for i in range(9) for j in range(9) if board[i,j] == 0]
        self.missing_rows = [list(range(9)) for x in range(10)]
        self.missing_cols = [list(range(9)) for x in range(10)]
        self.missing_squs = [list(range(9)) for x in range(10)]
        #missing_rows[x] contains rows which still miss x etc (ignoring missing_rows[0)


    def print_board(self):
        for i in range(9):
            row=''
            for j in range(9):
                row += str(self.board[i,j]) + ' '
                if j in [2,5]: row += '| '
            print(row)
            if i in [2,5]:
                print('---------------------')

        #print(self.board)

    def fill_number(self,i,j,x):
        self.board[i][j] = x
        self.update_candidates(i, j)
        #print("Filled ", x, " into field (", i, j, ")!")


    def fill_numbers(self):
        """
        fills in all empty fields with unique candidates
        :return: 0 if nothing changed, 1 if we filled numbers, 2 if unsolvable
        """

        flag = 0
        empty_fields = list(self.empty_fields)
        for (i,j) in empty_fields:
            cands = self.candidates[i][j]
            if len(cands) == 0: return 2
            if len(cands) == 1:
                self.fill_number(i,j,cands[0])
                flag = 1

        for x in range(1,10):
            for row in self.missing_rows[x]:
                cands = self.row_candidates[x][row]
                if len(cands) == 0:
                    return 2
                if len(cands) == 1:
                    self.fill_number(row, cands[0], x)
                    flag = 1

            for col in self.missing_cols[x]:
                cands = self.col_candidates[x][col]
                if len(cands) == 0:
                    return 2
                if len(cands) == 1:
                    self.fill_number(cands[0], col, x)
                    flag = 1

            for squ in self.missing_squs[x]:
                cands = self.squ_candidates[x][squ]
                if len(cands) == 0:
                    return 2
                if len(cands) == 1:
                    (i,j) = to_big_square(squ,cands[0])
                    self.fill_number(i, j, x)
                    flag = 1

        return flag

    def update_candidates(self, i, j, verbose=0):
        if verbose:
            print('For debugging')
        x = self.board[i,j]
        if x != 0:

            try: self.empty_fields.remove((i,j))
            except ValueError: pass

            for (ii,jj) in find_block(i, j):
                try: self.candidates[ii][jj].remove(x)
                except ValueError: pass

            for k in range(9):
                try: self.candidates[i][k].remove(x)
                except ValueError: pass
                try: self.candidates[k][j].remove(x)
                except ValueError: pass

            self.candidates[i][j].append(x)

            try: self.missing_rows[x].remove(i)
            except ValueError: pass
            try: self.missing_cols[x].remove(j)
            except ValueError: pass
            (ii, jj) = to_small_square(i, j)
            try: self.missing_squs[x].remove(ii)
            except ValueError: pass


            # remove field (i,j) as candidate for all other x
            for y in range(1,10):
                if y == x: continue

                try: self.row_candidates[y][i].remove(j)
                except ValueError: pass

                try: self.col_candidates[y][j].remove(i)
                except ValueError: pass

                try: self.squ_candidates[y][ii].remove(jj)
                except ValueError: pass


            # Let's now remove all squ/row/col candidates which became blocked by (i,j)
            for k in range(9):

                try: self.row_candidates[x][k].remove(j)
                except ValueError: pass

                ii,jj = to_small_square(k,j)
                try: self.squ_candidates[x][ii].remove(jj)
                except ValueError: pass

                try: self.col_candidates[x][k].remove(i)
                except ValueError: pass

                ii,jj = to_small_square(i,k)
                try: self.squ_candidates[x][ii].remove(jj)
                except ValueError: pass

            self.row_candidates[x][i] = [j]
            self.col_candidates[x][j] = [i]
            ii, jj = to_small_square(i,j)
            self.squ_candidates[x][ii] = [jj]

    def solve(self):
        for i in range(9):
            for j in range(9):
                self.update_candidates(i,j)

        while True:
            flag = self.fill_numbers()
            if flag == 2:
                print('Not solvable')
                return 2
            if not flag: break


        if self.empty_fields:
            print('Could not solve :(')
        else:
            print('Solved!')

board = np.load('./test-sudokus/hard.npy')
my_sudoku = sudoku(board=board)
my_sudoku.solve()
my_sudoku.print_board()
