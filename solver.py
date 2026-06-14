import csv
import numpy as np

DEFAULT_LIST_PATH = r"C:\Users\<your_user_name>\.cache\kagglehub\datasets\rohanrao\sudoku\versions\1\sudoku.csv"


def read_puzzle_from_csv(file_path, line_number):
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == line_number:
                return row[0]
    return None


def print_puzzle_9x9(puzzle):
    for row_index, row in enumerate(puzzle):
        if row_index > 0 and row_index % 3 == 0:
            print("-" * 21)

        row_parts = []
        for col_index, num in enumerate(row):
            if col_index > 0 and col_index % 3 == 0:
                row_parts.append("|")
            row_parts.append(str(num))

        print(" ".join(row_parts))


def puzzle_string_to_grid(puzzle_string):
    if puzzle_string is None or len(puzzle_string) != 81:
        raise ValueError("Puzzle must be an 81-character string")
    return np.array([[int(puzzle_string[i + j * 9]) for i in range(9)] for j in range(9)], dtype=int)


def puzzle_grid_to_string(puzzle):
    return "".join(str(int(value)) for value in puzzle.reshape(-1))


def fill_dof_row(dof, row_index, value):
    z_index = value - 1
    dof[z_index, row_index, :] += 1
    return dof


def fill_dof_col(dof, col_index, value):
    z_index = value - 1
    dof[z_index, :, col_index] += 1
    return dof


def fill_dof_box(dof, box_row_index, box_col_index, value):
    z_index = value - 1
    dof[z_index, box_row_index * 3:(box_row_index + 1) * 3, box_col_index * 3:(box_col_index + 1) * 3] += 1
    return dof


def fill_dof(dof, row, col, value):
    dof = fill_dof_row(dof, row, value)
    dof = fill_dof_col(dof, col, value)
    box_row_index = row // 3
    box_col_index = col // 3
    dof = fill_dof_box(dof, box_row_index, box_col_index, value)
    return dof


def build_dof(puzzle):
    dof = np.zeros((9, 9, 9), dtype=int)
    for row in range(9):
        for col in range(9):
            value = int(puzzle[row, col])
            if value != 0:
                dof = fill_dof(dof, row, col, value)
    return dof


def solve_puzzle_grid(puzzle):
    puzzle = np.array(puzzle, dtype=int).copy()
    dof = build_dof(puzzle)
    dof_collapsed = np.count_nonzero(dof, axis=0)

    have_progress=True
    while have_progress:
        have_progress = False
        # method #1
        indices = np.argwhere((dof_collapsed == 8) & (puzzle == 0))
        if len(indices) > 0:

            row, col = indices[0]
            z_candidates = np.where(dof[:, row, col] == 0)[0]

            value = int(z_candidates[0] + 1)
            puzzle[row, col] = value
            #print(f"Filled {value} at ({row}, {col}) using method 1")
            dof = fill_dof(dof, row, col, value)
            dof_collapsed = np.count_nonzero(dof, axis=0)
            have_progress = True
        else:
            # method 2
            # iterate through Z planes
            for z in range(9):
                # make a copy of the current Z plane of DOF
                dof_plane = dof[z].copy()
                # increment the dof_plane wherever the puzzle has a non-zero value (since those are not candidates)
                dof_plane[puzzle != 0] += 1

                # iterate through rows
                for row in range(9):
                    # find number of lelements with value 0
                    zero_indices = np.where(dof_plane[row, :] == 0)[0]
                    if len(zero_indices) == 1:
                        col = zero_indices[0]
                        value = int(z + 1)
                        puzzle[row, col] = value
                        #print(f"Filled {value} at ({row}, {col}) using method 2 (row)")
                        dof = fill_dof(dof, row, col, value)
                        dof_collapsed = np.count_nonzero(dof, axis=0)
                        have_progress = True
                        break
                for columns in range(9):
                    zero_indices = np.where(dof_plane[:, columns] == 0)[0]
                    if len(zero_indices) == 1:
                        row = zero_indices[0]
                        value = int(z + 1)
                        puzzle[row, columns] = value
                        #print(f"Filled {value} at ({row}, {columns}) using method 2 (column)")
                        dof = fill_dof(dof, row, columns, value)
                        dof_collapsed = np.count_nonzero(dof, axis=0)
                        have_progress = True
                        break
                # for all 9 boxes
                for box_row in range(3):
                    for box_col in range(3):
                        zero_indices = np.where(dof_plane[box_row * 3:(box_row + 1) * 3, box_col * 3:(box_col + 1) * 3] == 0)
                        if len(zero_indices[0]) == 1:
                            row = zero_indices[0][0] + box_row * 3
                            col = zero_indices[1][0] + box_col * 3
                            value = int(z + 1)
                            puzzle[row, col] = value
                            #print(f"Filled {value} at ({row}, {col}) using method 2 (box)")
                            dof = fill_dof(dof, row, col, value)
                            dof_collapsed = np.count_nonzero(dof, axis=0)
                            have_progress = True
                            break
        if not have_progress:# or np.count_nonzero(puzzle == 0) == 0:
            break

    solved = not np.any(puzzle == 0)
    return puzzle, solved, dof_collapsed


def solve_puzzle_string(puzzle_string):
    puzzle = puzzle_string_to_grid(puzzle_string)
    solved_puzzle, solved, _ = solve_puzzle_grid(puzzle)
    return puzzle_grid_to_string(solved_puzzle), solved


if __name__ == "__main__":
    puzzle_number = 1
    puzzle_string = read_puzzle_from_csv(DEFAULT_LIST_PATH, puzzle_number)
    if puzzle_string is None:
        print(f"Line number {puzzle_number} is out of range.")
    else:
        puzzle = puzzle_string_to_grid(puzzle_string)
        print_puzzle_9x9(puzzle)
        print("==============================")
        solved_puzzle, solved, dof_collapsed = solve_puzzle_grid(puzzle)
        print_puzzle_9x9(solved_puzzle)
        print("==============================")
        print_puzzle_9x9(dof_collapsed)
        print(f"Solved: {solved}")

