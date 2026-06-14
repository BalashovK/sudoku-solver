import csv
from itertools import chain

from solver import get_dataset_path, solve_puzzle_string


def solve_all(list_path=None, report_every=100):
	list_path = list_path or get_dataset_path()
	solved_count = 0
	unsolved_count = 0
	processed_count = 0

	with open(list_path, "r", newline="") as file:
		reader = csv.reader(file)
		first_row = next(reader, None)
		if first_row is None:
			print("No puzzles found.")
			return solved_count, unsolved_count, processed_count
		

		has_header = (
			len(first_row) >= 2
			and first_row[0].strip().lower() == "puzzle"
			and first_row[1].strip().lower() == "solution"
		)

		data_rows = reader if has_header else chain([first_row], reader)

		for row in data_rows:
			if len(row) < 2:
				continue

			puzzle_string = row[0].strip()
			expected_solution = row[1].strip()

			processed_count += 1
			try:
				solved_string, _ = solve_puzzle_string(puzzle_string)
			except ValueError:
				unsolved_count += 1
				continue

			if solved_string == expected_solution:
				solved_count += 1
			else:
				unsolved_count += 1

			if processed_count % report_every == 0:
				print(f"Processed {processed_count}: solved={solved_count}, unsolved={unsolved_count}")

	print("==============================")
	print(f"Processed {processed_count}: solved={solved_count}, unsolved={unsolved_count}")
	return solved_count, unsolved_count, processed_count


if __name__ == "__main__":
	solve_all()

