import re
import sys
from pathlib import Path
import shutil


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)

    t_name = re.sub(r'\W', "_", t_name)
    return t_name

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []


AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []


DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []


MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []


ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []

MY_OTHER = []

REGISTER_OF_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    "PNG": PNG_IMAGES,
    "JPG": JPG_IMAGES,
    "SVG": SVG_IMAGES,

    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,

    "DOC": DOC_DOCUMENTS,
    "DOCX": DOCX_DOCUMENTS,
    "TXT": TXT_DOCUMENTS,
    "PDF": PDF_DOCUMENTS,
    "XLSX": XLSX_DOCUMENTS,
    "PPTX": PPTX_DOCUMENTS,

    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,

    "ZIP": ZIP_ARCHIVES,
    "GZ": GZ_ARCHIVES,
    "TAR": TAR_ARCHIVES,
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("archives", "video", "audio", "documents", "images", "MY_OTHER"):
                FOLDERS.append(item)
                scan(item)
            continue

        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            MY_OTHER.append(fullname)

        else:
            try:
                container = REGISTER_OF_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)
def move_media(filename: Path,target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    normalized_filename = normalize(filename.stem) + filename.suffix
    filename.replace(target_folder / normalized_filename)

def handle_other(filename: Path,target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    normalized_filename = normalize(filename.stem) + filename.suffix
    filename.replace(target_folder / normalized_filename)

def handle_archive(filename: Path, target_folder:Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
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
    scan(folder)
    for file in JPEG_IMAGES:
        move_media(file, folder / "images" / 'JPEG')
    for file in PNG_IMAGES:
        move_media(file, folder / "images" / "PNG")
    for file in JPG_IMAGES:
        move_media(file, folder / "images" / "JPG")
    for file in SVG_IMAGES:
        move_media(file, folder / "images" / "SVG")

    for file in AVI_VIDEO:
        move_media(file, folder / "video" / "AVI")
    for file in MP4_VIDEO:
        move_media(file, folder / "video" / "MP4")
    for file in MOV_VIDEO:
        move_media(file, folder / "video" / "MOV")
    for file in MKV_VIDEO:
        move_media(file, folder / "video" / "MKV")

    for file in DOC_DOCUMENTS:
        move_media(file, folder / "documents" / "DOC")
    for file in DOCX_DOCUMENTS:
        move_media(file, folder / "documents" / "DOCX")
    for file in TXT_DOCUMENTS:
        move_media(file, folder / "documents" / "TXT")
    for file in PDF_DOCUMENTS:
        move_media(file, folder / "documents" / "PDF")
    for file in XLSX_DOCUMENTS:
        move_media(file, folder / "documents" / "XLSX")
    for file in PPTX_DOCUMENTS:
        move_media(file, folder / "documents" / "PPTX")

    for file in MP3_AUDIO:
        move_media(file, folder / "audio" / "MP3")
    for file in OGG_AUDIO:
        move_media(file, folder / "audio" / "OGG")
    for file in WAV_AUDIO:
        move_media(file, folder / "audio" / "WAV")
    for file in AMR_AUDIO:
        move_media(file, folder / "audio" / "AMR_AUDIO")

    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / "archives" / "ZIP")
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / "archives" / "GZ")
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / "archives" / "TAR")

    for file in MY_OTHER:
        handle_other(file, folder / "MY_OTHER")


    for folder in FOLDERS[::-1]:
        handle_folder(folder)

if sys.argv[1]:
    folder_for_scan = Path(sys.argv[1])
    print(f"Start in folder: {folder_for_scan.resolve()}")
    main(folder_for_scan.resolve())
