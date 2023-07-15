import sys
from pathlib import Path
import clean_folder as f


def start():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        f.main(folder_for_scan.resolve())

start()
