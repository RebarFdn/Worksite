# date: 2026-03-28
from pathlib import Path


# Application utilities and helper functions

# Function to check and create necessary directories
def check_paths( path:Path|None=None, paths:list=[]):    
    if paths:
        for path_item in paths:
            if not path_item.exists():
                print(f'Path {path_item} does not exist. Creating it now.')
                path_item.mkdir(parents=True, exist_ok=True)
    if path:
        if not path.exists():
            print(f'Path {path} does not exist. Creating it now.')
            path.mkdir(parents=True, exist_ok=True)

