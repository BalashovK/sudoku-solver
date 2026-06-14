from pathlib import Path

from solver import print_puzzle_9x9, puzzle_string_to_grid, solve_puzzle_string


file_to_solve = "puzzles/4.txt"


def load_puzzle(file_path):
    """Read a multi-row Sudoku puzzle and remove spaces/blank lines."""
    lines = [line.strip() for line in Path(file_path).read_text().splitlines() if line.strip()]
    return "".join("".join(lines).split())


def main():
    puzzle_string = load_puzzle(file_to_solve)
    original_grid = puzzle_string_to_grid(puzzle_string)
    solved_string, solved = solve_puzzle_string(puzzle_string)
    solved_grid = puzzle_string_to_grid(solved_string)

    print("Original puzzle:")
    print_puzzle_9x9(original_grid)
    print("\nSolved puzzle:")
    print_puzzle_9x9(solved_grid)
    print("\nSolved:", solved)


if __name__ == "__main__":
    main()


