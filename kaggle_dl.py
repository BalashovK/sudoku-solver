import kagglehub

# Download latest version
path = kagglehub.dataset_download("rohanrao/sudoku")

print("Path to dataset files:", path)