# Домашнее задание
## Задача
В этом домашнем задании мы сделаем из скрипта разбора папки Python-пакет и консольный скрипт, который можно вызывать в любом месте системы из консоли командой clean-folder. Для этого вам надо создать структуру файлов и папок:

## ├── clean_folder
## │    ├── clean_folder
## │    │   ├── clean.py
## │    │   └── __init__.py
## │    └── setup.py"


В clean_folder/clean_folder/clean.py нужно поместить всё, что мы сделали на предыдущих домашних заданиях по разбору папки. Ваша основная задача написать clean_folder/setup.py, чтобы встроенный инструментарий Python мог установить этот пакет и операционная система могла использовать этот пакет как консольную команду.

## Критерии приёма задания
Пакет устанавливается в систему командой pip install -e . (или python setup.py install, нужны права администратора).
После установки в системе появляется пакет clean_folder.
Когда пакет установлен в системе скрипт можно вызвать в любом месте из консоли командой clean-folder
Консольный скрипт обрабатывает аргументы командной строки точно так же, как и Python-скрипт.
