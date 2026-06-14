import csv
from itertools import chain

from solver import DEFAULT_LIST_PATH, print_puzzle_9x9, puzzle_grid_to_string, puzzle_string_to_grid, solve_puzzle_grid


def print_first_unsolved(list_path=DEFAULT_LIST_PATH, report_every=100):
	with open(list_path, "r", newline="") as file:
		reader = csv.reader(file)
		first_row = next(reader, None)
		if first_row is None:
			print("No puzzles found.")
			return None

		has_header = (
			len(first_row) >= 2
			and first_row[0].strip().lower() == "puzzle"
			and first_row[1].strip().lower() == "solution"
		)

		data_rows = reader if has_header else chain([first_row], reader)
		row_offset = 1 if has_header else 0

		for puzzle_index, row in enumerate(data_rows, start=0):
			if len(row) < 2:
				continue

			if puzzle_index > 0 and puzzle_index % report_every == 0:
				print(f"Checked {puzzle_index} puzzles...")

			puzzle_string = row[0].strip()
			expected_solution = row[1].strip()

			try:
				puzzle = puzzle_string_to_grid(puzzle_string)
			except ValueError:
				continue

			solved_puzzle, solved, dof_collapsed = solve_puzzle_grid(puzzle)
			solved_string = puzzle_grid_to_string(solved_puzzle)

			# Stop on the first puzzle that the solver does not finish correctly.
			if (not solved) or (solved_string != expected_solution):
				csv_line_number = puzzle_index + row_offset
				zeros_left = int((solved_puzzle == 0).sum())

				print("==============================")
				print(f"First unsolved puzzle found at CSV line: {csv_line_number}")
				print(f"Puzzle index (0-based, excluding header): {puzzle_index}")
				print(f"Solved flag: {solved}")
				print(f"Zeros left: {zeros_left}")
				print(f"Matches expected solution: {solved_string == expected_solution}")

				print("------------------------------")
				print("Original puzzle:")
				print_puzzle_9x9(puzzle)

				print("------------------------------")
				print("State left by solver:")
				print_puzzle_9x9(solved_puzzle)

				print("------------------------------")
				print("DOF collapsed at stop:")
				print_puzzle_9x9(dof_collapsed)

				return {
					"csv_line_number": csv_line_number,
					"puzzle_index": puzzle_index,
					"solved": solved,
					"zeros_left": zeros_left,
				}

	print("All puzzles solved by current algorithm.")
	return None


if __name__ == "__main__":
	print_first_unsolved()

