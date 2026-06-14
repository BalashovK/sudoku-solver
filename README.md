# sudoku-solver

Solver for Sudoky

## Does is solve all sudokus?

No, but it solves most. At least it solves more than I.

## Where to start?

run solve_one.py

it reads a sudoku and solves it. 

## Where is the solver code?

in solver.py

## What are the other files?

kaggle_dl.py downloads 9 million sudoku from kaggle

you need to update DEFAULT_LIST_PATH in solver to use it (sorry, I was too lazy to ask Copilot to connect the dots)

solve_all.py tries to solve them all

print_first_unsolved.py prints the first one it cannot solve

## Data format

this software reads 2 data formats:

070000043040009610800634900094052000358460020000800530080070091902100005007040802

which is array of 81 digits to be reshaped into 9x9

and 

030 009 012
080 000 000
620 080 004

850 302 700
000 000 000
002 901 068

700 090 023
000 000 080
460 100 050

which is more human-readable.
 