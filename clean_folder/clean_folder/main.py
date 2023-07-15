from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize

def move_media(filename: Path,target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    normalized_filename = normalize(filename.stem) + filename.suffix
    filename.replace(target_folder / normalized_filename)

def handle_other(filename: Path,target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    normalized_filename = normalize(filename.stem) + filename.suffix
    filename.replace(target_folder / normalized_filename)

def handle_archive(filename: Path, target_folder:Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True) # создаём папку для архива
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ""))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print("It is not archive")
        folder_for_file.rmdir()
    filename.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        move_media(file, folder / "images" / 'JPEG')
    for file in parser.PNG_IMAGES:
        move_media(file, folder / "images" / "PNG")
    for file in parser.JPG_IMAGES:
        move_media(file, folder / "images" / "JPG")
    for file in parser.SVG_IMAGES:
        move_media(file, folder / "images" / "SVG")

    for file in parser.AVI_VIDEO:
        move_media(file, folder / "video" / "AVI")
    for file in parser.MP4_VIDEO:
        move_media(file, folder / "video" / "MP4")
    for file in parser.MOV_VIDEO:
        move_media(file, folder / "video" / "MOV")
    for file in parser.MKV_VIDEO:
        move_media(file, folder / "video" / "MKV")

    for file in parser.DOC_DOCUMENTS:
        move_media(file, folder / "documents" / "DOC")
    for file in parser.DOCX_DOCUMENTS:
        move_media(file, folder / "documents" / "DOCX")
    for file in parser.TXT_DOCUMENTS:
        move_media(file, folder / "documents" / "TXT")
    for file in parser.PDF_DOCUMENTS:
        move_media(file, folder / "documents" / "PDF")
    for file in parser.XLSX_DOCUMENTS:
        move_media(file, folder / "documents" / "XLSX")
    for file in parser.PPTX_DOCUMENTS:
        move_media(file, folder / "documents" / "PPTX")

    for file in parser.MP3_AUDIO:
        move_media(file, folder / "audio" / "MP3")
    for file in parser.OGG_AUDIO:
        move_media(file, folder / "audio" / "OGG")
    for file in parser.WAV_AUDIO:
        move_media(file, folder / "audio" / "WAV")
    for file in parser.AMR_AUDIO:
        move_media(file, folder / "audio" / "AMR_AUDIO")

    for file in parser.ZIP_ARCHIVES:
        handle_archive(file, folder / "archives" / "ZIP")
    for file in parser.GZ_ARCHIVES:
        handle_archive(file, folder / "archives" / "GZ")
    for file in parser.TAR_ARCHIVES:
        handle_archive(file, folder / "archives" / "TAR")

    for file in parser.MY_OTHER:
        handle_other(file, folder / "MY_OTHER")


    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f"Start in folder: {folder_for_scan.resolve()}")
        main(folder_for_scan.resolve())
