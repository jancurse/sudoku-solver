from help_functions import *
import numpy as np
import copy


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

    def solve(self, verbose=1):
        solvable = 1
        for i in range(9):
            for j in range(9):
                self.update_candidates(i,j)

        while True:
            flag = self.fill_numbers()
            if flag == 2:
                if verbose: print('Not solvable')
                return 0
            if flag == 0: break

        # If we are not done, we start making educated guesses
        if self.empty_fields:
            # find a good empty field to guess
            best_field, best_value = (0,0), 10
            for (i,j) in self.empty_fields:
                if len(self.candidates[i][j]) < best_value:
                    best_field = (i,j)
                    best_value = len(self.candidates[i][j])
                    if best_value == 2: break

            for x in self.candidates[i][j]:
                help_sudoku = copy.deepcopy(self)
                help_sudoku.fill_number(i,j,x)
                help_solvable = help_sudoku.solve(verbose=0)
                if help_solvable:
                    self.__dict__ = help_sudoku.__dict__.copy()
                    break

        if verbose: print('Solved!')
        return 1
