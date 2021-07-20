import pathlib
from typing import Union, Optional, List, Tuple, Generator
from os import path, makedirs, listdir, remove
import shutil
from subprocess import Popen
from platform import system

DIRIN = path.abspath(path.join("..", "Materialsammlung"))
DIROUT = path.abspath(path.join("..", "aktuelle_Unterrichtsvorbereitung"))
EXTS = [ '.pdf', '.doc', '.docx', '.pptx', '.txt' ]

makedirs(DIRIN, exist_ok=True)
makedirs(DIROUT, exist_ok=True)

class FILE:
    def __init__(self, rpath: str, fid: Optional[int] = None, mtime: Optional[int] = None, tags: Optional[List[Tuple[int, str]]] = None, prio: Optional[int] = None):
        """
        Constructor:
          fpath: Pfad string in relativem Verhältnis zu DIRIN
          fid:   Datenbank file primary key
          tags:  bekannte tag match referenz Liste
                 eine Referenz ist ein Tuple mit einem int und einem str:
                 int: seltionsnummer in dem der tag vorkommt
                 str: der gematchte tag
        """
        self.id: int = fid or -1
        self.name = path.basename(rpath)
        self.path = path.dirname(rpath)
        self.mtime = mtime if mtime is not None else 0
        self.type = path.splitext(self.name)[1].lower()
        self.tags = tags if tags else []
        self.prio = prio if prio is not None else 0

    def full_path(self):
        "Gibt den absoluten Pfad der Datei zurück"
        return path.abspath(path.join(DIRIN, self.__repr__()))

    def view_name_ui(self):
        """Gibt den Dateinamen und den darüber liegenden Ordner zurück"""
        fullpath = path.abspath(path.join(DIRIN, self.__repr__()))
        filename = fullpath.split("\\")
        return f"{filename[-2]}\\{filename[-1]}"

    def peek(self, loc: Union[int, Tuple[int, str]], scope: int):
        """
        Gibt den Kontext des gematchten Tags als string zurück
        Wenn type(loc) is int: nimmt es self.tags[loc].
        Ansonsten kann loc auch ein element aus self.tags sein.
        """
        pass

    def open(self):
        "Öffnet self.full_path in der vom System gesetzten Standartanwendung"
        if system() == "Linux":
            Popen(['xdg-open', self.full_path()], stdin=None, stdout=None, stderr=None, close_fds=True)
        elif system() == "Windows":
            Popen(['start', self.full_path()], stdin=None, stdout=None, stderr=None, close_fds=True)
        else:
            Popen(['open', self.full_path()], stdin=None, stdout=None, stderr=None, close_fds=True)

    def __repr__(self) -> str:
        return path.join(self.path, self.name)

    def result(self) -> str:
        return f"{self.prio}\t{self.__repr__()}"

    def __gt__(self, other) -> bool:
        return self.__repr__() > other.__repr__()

def search_files(pathlist: List[str]) -> Generator[Tuple[str, int], None, None]:
    """
      Generator nimmt eine Liste an Ordnern und gibt relative Pfade (zu DIRIN) und deren mtime aus.

      +------------+
      | Parameter |
      +------------+
      | pathlist: List[str]
      |   Liste von Ordnern.
    """
    for fpath in pathlist:
        if path.isfile(fpath):
            yield (path.relpath(fpath, start=DIRIN), int(path.getmtime(fpath)))
            continue
        elif path.isdir(fpath):
            yield from search_files([path.join(fpath, x) for x in listdir(fpath)])
            continue
        print(f"[WARN]: No such file or directory: {fpath}")


def exists_not(plist: List[str]) -> List[str]:
    return [p for p in plist if not path.exists(path.join(DIRIN, p))]

def clear() -> bool:
    try:
        for elem in listdir(DIROUT):
            if path.isfile(path.join(DIROUT, elem)):
                remove(path.join(DIROUT, elem))
        return True
    except OSError as err:
        print(f"Error during file removal in {DIROUT}\nERR: {err}")
        return False

def copy(src) -> bool:
    try:
        shutil.copy(path.join(DIRIN, src), DIROUT)
        return True
    except OSError as err:
        print("Error while copying {src} to {DIROUT}\nERR: {err}")
        return False
