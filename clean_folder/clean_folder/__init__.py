from pathlib import Path
import sys
import clean_folder.main

def start_work():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f"Start in folder: {folder_for_scan.resolve()}")
        clean_folder.main.main(folder_for_scan.resolve())
    else:
        current_path = Path('.')
        print(f"Start in current folder: {folder_for_scan.resolve()}")
        clean_folder.main.main(current_path.resolve())
