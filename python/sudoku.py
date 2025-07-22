from typing import List

NUM_CELLS = 81
NUM_DIGITS = 9

groups = [
    [ 0,  1,  2,  3,  4,  5,  6,  7,  8],
    [ 9, 10, 11, 12, 13, 14, 15, 16, 17],
    [18, 19, 20, 21, 22, 23, 24, 25, 26],
    [27, 28, 29, 30, 31, 32, 33, 34, 35],
    [36, 37, 38, 39, 40, 41, 42, 43, 44],
    [45, 46, 47, 48, 49, 50, 51, 52, 53],
    [54, 55, 56, 57, 58, 59, 60, 61, 62],
    [63, 64, 65, 66, 67, 68, 69, 70, 71],
    [72, 73, 74, 75, 76, 77, 78, 79, 80],
    [ 0,  9, 18, 27, 36, 45, 54, 63, 72],
    [ 1, 10, 19, 28, 37, 46, 55, 64, 73],
    [ 2, 11, 20, 29, 38, 47, 56, 65, 74],
    [ 3, 12, 21, 30, 39, 48, 57, 66, 75],
    [ 4, 13, 22, 31, 40, 49, 58, 67, 76],
    [ 5, 14, 23, 32, 41, 50, 59, 68, 77],
    [ 6, 15, 24, 33, 42, 51, 60, 69, 78],
    [ 7, 16, 25, 34, 43, 52, 61, 70, 79],
    [ 8, 17, 26, 35, 44, 53, 62, 71, 80],
    [ 0,  1,  2,  9, 10, 11, 18, 19, 20],
    [ 3,  4,  5, 12, 13, 14, 21, 22, 23],
    [ 6,  7,  8, 15, 16, 17, 24, 25, 26],
    [27, 28, 29, 36, 37, 38, 45, 46, 47],
    [30, 31, 32, 39, 40, 41, 48, 49, 50],
    [33, 34, 35, 42, 43, 44, 51, 52, 53],
    [54, 55, 56, 63, 64, 65, 72, 73, 74],
    [57, 58, 59, 66, 67, 68, 75, 76, 77],
    [60, 61, 62, 69, 70, 71, 78, 79, 80],
]

class SudokuSolver:
    assignments = 0
    unassignments = 0
    def __init__(self):
        self.cells = [None] * NUM_CELLS
        self.available_digits = [[True] * NUM_DIGITS for _ in range(NUM_CELLS)]
        self.in_group = [[] for _ in range(NUM_CELLS)]
        self.propagations = []
        for group in groups:
            for cell in group:
                self.in_group[cell].append(group)
    def solve(self, idx=0):
        if idx >= NUM_CELLS:
            return True
        if self.cells[idx] != None:
            if self.solve(idx + 1):
                return True
        for value, available in enumerate(self.available_digits[idx]):
            if available:
                if self.set(idx, value):
                    if self.solve(idx + 1):
                        return True
                self.unset(idx, value)
        return False
    def set(self, idx, value) -> bool:
        self.assignments += 1
        self.cells[idx] = value
        propagations = []
        self.propagations.append(propagations)
        for group in self.in_group[idx]:
            for cell in group:
                if cell != idx and self.available_digits[cell][value]:
                    self.available_digits[cell][value] = False
                    propagations.append((cell, value))
                    if not any(self.available_digits[cell]):
                        return False
        return True
    def unset(self, idx, value):
        self.unassignments += 1
        self.cells[idx] = None
        for shared_cell, value in self.propagations.pop():
            self.available_digits[shared_cell][value] = True

def get_leetcode_result(solver: SudokuSolver):
    rows = []
    row = []
    for idx, val in enumerate(solver.cells):
        if idx!= 0 and idx % 9 == 0:
            rows.append(row)
            row = []
        row.append(str(val+1))
    rows.append(row)
    return rows

def parse_leetcode_input(board: list[list[str]]):
    return [int(cell) if cell != "." else None for row in board for cell in row]

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        solver = SudokuSolver()
        for idx, value in enumerate(parse_leetcode_input(board)):
            if value:
                solver.set(idx, value-1)
        solver.solve()
        board.clear()
        board.extend(get_leetcode_result(solver))
    def solveSudokuLocal(self, puzzle_string):
        import time
        start = time.time()
        solver = SudokuSolver()
        for idx, char in enumerate(puzzle_string):
            if char != ".":
                solver.set(idx, int(char)-1)
        print(solver.available_digits)
        solver.solve()
        end = time.time()
        print("assignments", solver.assignments)
        print("unassignment", solver.unassignments)
        print("time (seconds)", end-start)
  
Solution().solveSudokuLocal("4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........")
