from pathlib import Path

PATH_NE = "der pfad '{}' existiert nicht"
PATH_NFI = "der pfad '{}' ist ein File, es wird jedoch ein Ordner erwartet"
PATH_NFO = "der pfad '{}' ist ein Ordner, es wird jedoch ein File erwartet"
PATH_WFF = "der File '{}' hat ein falsches format erwartet wird '{}'"

PQT_FST = "file:///"
"""
    Überprüft ob ein pfad existiert und den richtigen typen hat

Attribute:
    Path: Der zu prüfende Pfad
    is_folder: True wenn der Pfad ein Ordner sein Soll False wenn es ein File sein soll
    type: Welcher typ der File haben sollte z.B '.CSV' (Endung des Files)
"""
def is_path_valid(path : Path,is_folder : bool, type : str = None):

    #Überprüfung ob es ein Ordner/File ist, je nachdem was bei is_folder übergeben wurde
    if path.is_dir() != is_folder:
        if is_folder:
            raise FileNotFoundError(PATH_NFI.format(path))
        else:
            raise FileNotFoundError(PATH_NFO.format(path))

    #Überprüfung ob der Pfad existiert
    if not path.exists():
        raise FileNotFoundError(PATH_NE.format(path))

    #Falls ein Ordner zu prüfen war ist hier die prüfung zu ende
    if type is None:
        return

    #Überprüft ob der type mit '.' anfängt, damit die endung geprüft werden kann
    if not type.startswith("."):
        type = '.' + type

    #Überprüft ob der Pfad die richtige endung hat
    if not path.as_posix().endswith(type):
        raise FileNotFoundError(PATH_WFF.format(path,type))


"""
    Überprüft ob der File existiert und ob es ein File ist

Attribute
    path: Der zu prüfende Pfad
    type: Welcher typ der File haben sollte z.B '.CSV' (Endung des Files)
"""
def is_file_valid(path : Path, type : str = None):
    try:
        is_path_valid(path,False,type)
    except Exception as e:
        raise e

"""
    Überprüft ob der Ordner Existiert 
    
Attribute
    path: Der zu prüfende Pfad
"""
def is_folder_valid(path : Path):
    try:
        is_path_valid(path,True,None)
    except Exception as e:
        raise e

"""
Wandelt den PyQt DropDown Event Handler in einen Path um

Attribute:
    event: Das aus dem DropDown resultierende event
    index: Index des zu holenden Pfades
"""
def event_path_to_path(event,index = 0):
    pyqt_path = event.mimeData().urls()[index]
    str_path = pyqt_path.toString().replace(PQT_FST, '')
    return Path(str_path)