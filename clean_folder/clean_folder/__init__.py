from pathlib import Path
import sys
from main import main

def start_work():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f"Start in folder: {folder_for_scan.resolve()}")
        main(folder_for_scan.resolve())
