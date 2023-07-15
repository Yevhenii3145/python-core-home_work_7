import sys
from pathlib import Path

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
    # преобразуем расширение файла на название папки. .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # если это папка то добавляем её к списку FOLDERS и переходим к следующему элементу папки
        if item.is_dir():
            # проверяем,чтобы папка не была той, в которую мы уже складываем файлы
            if item.name not in ("archives", "video", "audio", "documents", "images", "MY_OTHER"):
                FOLDERS.append(item)
                # сканируем вложенную папку
                scan(item)  # рекурсия
            continue  # перехдим к следующему элементу в сканированной папке

        # работа с файлом
        ext = get_extension(item.name)  # берём расширение файла
        fullname = folder / item.name  # берём путь к файлу
        if not ext:  # если файл не имеет расширение, то добавляем к неизвестным
            MY_OTHER.append(fullname)

        else:
            try:
                container = REGISTER_OF_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # если нет такого расширения в REGISTER_OF_EXTENSION, то добавляем к неизвестным
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


if __name__ == "__main__":
    folder_to_scan = sys.argv[1]
    print(f"Start in folder {folder_to_scan}")
    scan(Path(folder_to_scan))

    print(f"Images jpeg: {JPEG_IMAGES}")
    print(f"Images png: {PNG_IMAGES}")
    print(f"Images jpg: {JPG_IMAGES}")
    print(f"Images svg: {SVG_IMAGES}")

    print(f"Video avi: {AVI_VIDEO}")
    print(f"Video mp4: {MP4_VIDEO}")
    print(f"Video mov: {MOV_VIDEO}")
    print(f"Video mkv: {MKV_VIDEO}")

    print(f"Documents doc: {DOC_DOCUMENTS}")
    print(f"Documents docx: {DOCX_DOCUMENTS}")
    print(f"Documents txt: {TXT_DOCUMENTS}")
    print(f"Documents pdf: {PDF_DOCUMENTS}")
    print(f"Documents xlsx: {XLSX_DOCUMENTS}")
    print(f"Documents pptx: {PPTX_DOCUMENTS}")

    print(f"Audio mp3: {MP3_AUDIO}")
    print(f"Audio ogg: {OGG_AUDIO}")
    print(f"Audio wav: {WAV_AUDIO}")
    print(f"Audio amr: {AMR_AUDIO}")

    print(f"Archives zip: {ZIP_ARCHIVES}")
    print(f"Archives gz: {GZ_ARCHIVES}")
    print(f"Archives tar: {TAR_ARCHIVES}")

    print(f"My other: {MY_OTHER}")

    print(f"Types of files in folder: {EXTENSION}")
    print(f"Unknown types of files: {UNKNOWN}")
    print(FOLDERS[::-1])
