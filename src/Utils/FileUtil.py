from pathlib import Path

PATH_NE = "der pfad '{}' existiert nicht"
PATH_NFI = "der pfad '{}' ist ein File, es wird jedoch ein Ordner erwartet"
PATH_NFO = "der pfad '{}' ist ein Ordner, es wird jedoch ein File erwartet"
PATH_WFF = "der File '{}' hat ein falsches format erwartet wird '{}'"

def is_path_valid(path : Path,is_folder : bool, type : str = None):

    if path.is_dir() != is_folder:
        if is_folder:
            raise FileNotFoundError(PATH_NFI.format(path))
        else:
            raise FileNotFoundError(PATH_NFO.format(path))

    if not path.exists():
        raise FileNotFoundError(PATH_NE.format(path))

    if type is None:
        return

    if not type.startswith("."):
        type = '.' + type

    if not path.as_posix().endswith(type):
        raise FileNotFoundError(PATH_WFF.format(path,type))


def is_file_valid(path : Path, type : str = None):
    try:
        is_path_valid(path,False,type)
    except Exception as e:
        raise e

def is_folder_valid(path : Path, type : str = None):
    try:
        is_path_valid(path,True,type)
    except Exception as e:
        raise e