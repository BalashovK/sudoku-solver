import os
from pathlib import Path

import kagglehub


CONFIG_PATH = Path("data.config")

# Download latest version
path = kagglehub.dataset_download("rohanrao/sudoku")
file_path = os.path.join(path, "sudoku.csv")

CONFIG_PATH.write_text(f"{file_path}\n", encoding="utf-8")

print("Path to dataset files:", path)
print("Saved CSV path to:", file_path)
print("Saved dataset path to:", CONFIG_PATH)
