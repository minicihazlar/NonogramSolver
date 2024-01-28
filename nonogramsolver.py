class NonogramSolver():
    def __init__(self, columns, rows):
        self._columns = columns
        self._rows = rows
        self._x_sz = len(columns)
        self._y_sz = len(rows)
        self._board = [[-1 for _ in range(self._x_sz)] for _ in range(self._y_sz)]
        self._boardtotal = self._get_total(columns)
    
    def print_solution(self):
        print('{}{}{}'.format(u'\u2554', u'\u2550' * self._x_sz * 2, u'\u2557'))
        for x in self._board:
            print(u'\u2551', end="")
            for i in x:
                if i == 1:
                    print(u'\u2593\u2593', end="")
                elif i == 0:
                    print("  ", end="")
                else:
                    print(u'\u2591\u2591', end="")
            print(u'\u2551')
        print('{}{}{}\n'.format(u'\u255A', u'\u2550' * self._x_sz * 2, u'\u255D'))

    def _get_total(self, lst):
        return sum([sum(i) for i in lst])
    
    def _get_possible(self, lst, sz):
        __cr = []
        if sz == 1:
            return [[1]] 
        for i in range(sz - sum(lst) - len(lst) + 2):
            if len(lst) == 1:
                __cr.append(([0] * i) + 
                            ([1] * lst[0]) + 
                            ([0] * (sz - i - lst[0])))
            else:
                tmp = self._get_possible(lst[1:], sz - i - lst[0] - 1)
                for item in tmp:                
                    __cr.append(([0] * i) + 
                                ([1] * lst[0]) + 
                                [0] + 
                                item)
        return __cr

    def _get_possibilities(self, lst, sz):
        colrow = []
        for cr in lst:
            # Check special case, where the column has already just a single possible solution
            if (sum(cr) + len(cr) - 1) == sz:
                _cr = []
                for i, val in enumerate(cr):
                    _cr += [1] * val
                    if i != (len(cr) - 1):
                        _cr += [0]
                colrow.append([_cr])
            # So no single solution for this specific column yet, just get all possibilities
            else:
                possibilities = self._get_possible(cr, sz)
                colrow.append(possibilities)
        return colrow

    def _eliminate_possibilities_that_are_impossible(self, c, r, val):
        for _c in self._columns_possibilities[c].copy():
            if _c[r] != val:
                self._columns_possibilities[c].remove(_c)
        for _r in self._rows_possibilities[r].copy(): 
            if _r[c] != val:
                self._rows_possibilities[r].remove(_r)

    def _check_columns_for_obvious_moves(self):
        for j, _col in enumerate(self._columns_possibilities):
            _c1 = [1 for _ in range(self._y_sz)] # To chech if all possible solutions have a 1 at a specific index
            _c2 = [0 for _ in range(self._y_sz)] # To chech if all possible solutions have a 0 at a specific index

            for c in _col:
                _c1 = [x & y for x, y in zip(_c1, c)] 
                _c2 = [x | y for x, y in zip(_c2, c)] 

            for i, val in enumerate(_c1):
                if val == 1:
                    self._board[i][j] = 1
                    self._eliminate_possibilities_that_are_impossible(j, i, 1)

            for i, val in enumerate(_c2):
                if val == 0:
                    self._board[i][j] = 0
                    self._eliminate_possibilities_that_are_impossible(j, i, 0)

    def _check_row_for_obvious_moves(self):
        for j, _row in enumerate(self._rows_possibilities):
            _r1 = [1 for _ in range(self._x_sz)] # To chech if all possible solutions have a 1 at a specific index
            _r2 = [0 for _ in range(self._x_sz)] # To chech if all possible solutions have a 0 at a specific index

            for r in _row:
                _r1 = [x & y for x, y in zip(_r1, r)] 
                _r2 = [x | y for x, y in zip(_r2, r)] 

            for i, val in enumerate(_r1):
                if val == 1:
                    self._board[j][i] = 1
                    self._eliminate_possibilities_that_are_impossible(i, j, 1)

            for i, val in enumerate(_r2):
                if val == 0:
                    self._board[j][i] = 0
                    self._eliminate_possibilities_that_are_impossible(i, j, 0)

    def solve(self):
        self._columns_possibilities = self._get_possibilities(self._columns, self._y_sz)
        self._rows_possibilities = self._get_possibilities(self._rows, self._x_sz)
        # Check if nonogram is completely solved, the total of ones in the board list should 
        # match to the total of either column or row values summed together
        localboardtotal = 0
        iteration = 0
        while self._boardtotal != localboardtotal: 
            self._check_columns_for_obvious_moves()
            # self.print_solution()
            self._check_row_for_obvious_moves()
            # self.print_solution()
            localboardtotaltmp = self._get_total(self._board)
            if localboardtotal == localboardtotaltmp:
                # Nothing changed, this means there is no unique solution
                print("No unique solution possible! So trying to select one possible solution...")
                found = False
                for c in self._columns_possibilities:
                    if found == True:
                        break
                    if len(c) != 1:
                        found = True
                        for i in c[1:].copy():
                            c.remove(i)                            
                if found == False:
                    for r in self._rows_possibilities:
                        if found == True:
                            break
                        if len(r) != 1:
                            found =True
                            for i in r[1:].copy():
                                r.remove(i)
                iteration += 1
                if iteration == 10:
                    break
            localboardtotal = localboardtotaltmp
        return self._board

if __name__ == '__main__':
    n_c =[[6,4], [9,4], [12,5], [20,5], [23,5], [8,13,3], [7,1,3,7,2], [8,2,2,8], [8,1,4,2,4], [9,1,1,2,2], [12,1,4], [13,1,2], [13,3,1], [14,2,2], [14,1,1], [13,2,2], [14,1,2], [14,2], [20,7], [17,1,11], [14,1,8], [12,1,11], [12,12,2], [24,2], [13,9,3], [8,9,1], [8,1], [7,2], [6,2], [4,1]] 
    n_r = [[6], [9], [11], [13], [16], [19], [23], [25], [25], [26], [26], [26], [6,16], [4,1,7,10], [4,1,8], [3,3,6,3,4], [3,1,1,2,1,2,3], [3,1,1,1,2,4], [3,1,1,1,3], [3,1,3,3], [3,1,1,3], [3,7], [3,2,9], [4,1,1,10], [4,1,1,11], [5,1,2,11], [4,3,12], [5,3,12], [8,12], [6,1,1,6], [4,2,1,1,2], [5,1,1,1,3], [8,2], [7,5], [6,3]]
    nonogram = NonogramSolver(n_c, n_r)
    nonogram.solve()
    nonogram.print_solution()

    n_c = [[1,1,2], [2,2,3], [1,2,4], [2,2,2], [2,2,4,2,2], [18,3], [2,1,5,3], [3,2,3,4,3,1], [6,4,6,8], [4,3,3,3,3], [3,3,1,3,1], [2,4,1,2,3,1], [1,2,2,1,1,2,3], [1,5,1,2,2], [3,2,2,1,1,3], [6,4,2,1,1,3], [6,2,2,2,8,3], [4,5,1,2,4], [1,2,1,2,1,6,2], [2,1,3,3,5,1,3], [2,3,1,1,4,6,1], [4,3,4,3,6], [4,1,2,12,1], [3,2,2], [3,5], [3,5], [2,1,3], [1,2,2], [1,1], [1,1]]
    n_r = [[1,2,2], [2,2,2], [2,3,2], [3,4,4], [4,4,4], [2,10,5], [3,3,5,3], [3,2,6,1,4], [4,11,4], [1,1,2,1,1,2,1,4], [5,11,4,6], [6,3,4,4,7], [6,1,3,1], [2,1,3,1], [2,1,3,1], [2,5,5], [2,3,1,2], [1,7,7], [2,2,3,2,3], [2,2,1,2,1], [2,2,1,4], [2,1,1,2,2], [2,3,3,5], [2,2,1,3,1], [5,1,2,1,3], [2,2,2,5], [2,2,8,2], [2,1,2,6,3], [3,2,2,6,1], [3,2,3,1,5]]
    nonogram = NonogramSolver(n_c, n_r)
    nonogram.solve()
    nonogram.print_solution()

    n_r = [[3], [2,1], [3,2], [2,2], [6], [1,5], [6], [1], [2]]
    n_c = [[1,2], [3,1], [1,5], [7,1], [5], [3], [4], [3]]
    nonogram = NonogramSolver(n_c, n_r)
    nonogram.solve()
    nonogram.print_solution()

    n_c = [[7,3,1,1,7], [1,1,2,2,1,1], [1,3,1,3,1,1,3,1], [1,3,1,1,6,1,3,1], [1,3,1,5,2,1,3,1], [1,1,2,1,1], [7,1,1,1,1,1,7], [3,3], [1,2,3,1,1,3,1,1,2], [1,1,3,2,1,1], [4,1,4,2,1,2], [1,1,1,1,1,4,1,3], [2,1,1,1,2,5], [3,2,2,6,3,1], [1,9,1,1,2,1], [2,1,2,2,3,1], [3,1,1,1,1,5,1], [1,2,2,5], [7,1,2,1,1,1,3], [1,1,2,1,2,2,1], [1,3,1,4,5,1], [1,3,1,3,10,2], [1,3,1,1,6,6], [1,1,2,1,1,2], [7,2,1,2,5]]
    n_r = [[7,2,1,1,7], [1,1,2,2,1,1], [1,3,1,3,1,3,1,3,1], [1,3,1,1,5,1,3,1], [1,3,1,1,4,1,3,1], [1,1,1,2,1,1], [7,1,1,1,1,1,7], [1,1,3], [2,1,2,1,8,2,1], [2,2,1,2,1,1,1,2], [1,7,3,2,1], [1,2,3,1,1,1,1,1], [4,1,1,2,6], [3,3,1,1,1,3,1], [1,2,5,2,2], [2,2,1,1,1,1,1,2,1], [1,3,3,2,1,8,1], [6,2,1], [7,1,4,1,1,3], [1,1,1,1,4], [1,3,1,3,7,1], [1,3,1,1,1,2,1,1,4], [1,3,1,4,3,3], [1,1,2,2,2,6,1], [7,1,3,2,1,1]]    
    nonogram = NonogramSolver(n_c, n_r)
    nonogram.solve()
    nonogram.print_solution()
