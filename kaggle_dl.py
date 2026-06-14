from pathlib import Path

import kagglehub


CONFIG_PATH = Path("data.config")

# Download latest version
path = kagglehub.dataset_download("rohanrao/sudoku")

CONFIG_PATH.write_text(f"{path}\n", encoding="utf-8")

print("Path to dataset files:", path)
print("Saved dataset path to:", CONFIG_PATH)
