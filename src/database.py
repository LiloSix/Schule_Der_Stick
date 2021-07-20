import sqlite3
from os.path import sep
import atexit
from typing import List, Tuple, Union, Optional

CON = sqlite3.connect('index.db')
CUR = CON.cursor()
DBSEP = "/"

def tag_add(tag) -> bool:
    "Fügt neuen Tag hinzu"
    try:
        CUR.execute("INSERT INTO Tags (Tag) VALUES (?)", (tag,))
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL tag_add Error\nERR: {err}")
        return False


def tag_remove(tag) -> bool:
    "Entfernt Tag aus Datenbank"
    try:
        CUR.execute("DELETE FROM Tags WHERE Tag = ?", (tag, ))
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL tag_remove Error\nERR: {err}")
        return False


def tag_hint(tag: str) -> List[str]:
    "Autovervollständigung für Tags"
    try:
        return list([x[0] for x in CUR.execute("SELECT Tag FROM Tags WHERE Tag LIKE ?", (f"%{tag}%", ))])
    except sqlite3.Error as err:
        print(f"SQL tag_hint Error\nERR: {err}")
        return []


def format_files_get(files: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    "Formatiert Pfad Strings system agnostisch"
    return list((fpath.replace(DBSEP, sep), fid, lind) for (fpath, fid, lind) in files)


def files_get() -> List[Tuple[str, int, int]]:
    "Gibt alle in der Datenbank registrierten Dateien zurück (Pfad, ID, letzte Aktualisierung)"
    try:
        return format_files_get(list(CUR.execute("SELECT FilePath, FileID, LastIndexed FROM Files")))
    except sqlite3.Error as err:
        print(f"SQL files_get Error\nERR: {err}")
        return []


def files_get_due() -> List[Tuple[str, int, int]]:
    """
    Gibt alle Dateien zurück für die mindestens ein zu Indexierender Tag existiert
    """
    try:
        files = CUR.execute("SELECT FilePath, FileID, LastIndexed FROM Files WHERE (SELECT TagAdded FROM Tags ORDER BY TagAdded DESC LIMIT 1) > LastIndexed")
        return format_files_get(list(files))
    except sqlite3.Error as err:
        print(f"SQL files_get Error\nERR: {err}")
        return []

def files_get_select(fid: List[int]) -> List[Tuple[str, int, int]]:
    try:
        files = CUR.execute("SELECT FilePath, FileID, LastIndexed FROM Files WHERE FileID IN ({param})".format(
            param=','.join(['?']*len(fid))), tuple(fid))
        return format_files_get(list(files))
    except sqlite3.Error as err:
        print(f"SQL files_get_select Error\nERR: {err}")
        return []


def files_add(files: List[Tuple[str, int]]) -> bool:
    files = [(path.replace(sep, DBSEP), itime) for (path, itime) in files]
    try:
        CUR.executemany("INSERT INTO Files (FilePath, LastIndexed) VALUES (?, ?)", files)
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL files_add Error\nERR: {err}")
        return False


def files_get_new(fpath: List[str]):
    try:
        knownpaths = [p.replace(DBSEP, sep) for p in CUR.execute("SELECT FilePath FROM Files")]
        return list(p for p in fpath if p not in knownpaths)
    except sqlite3.Error as err:
        print(f"SQL files_get_new Error\nERR: {err}")
        return []


def files_clear() -> bool:
    try:
        CUR.execute("DELETE FROM Files")
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL filetags_clear Error\nERR: {err}")
        return False


def files_clear_select(fid: List[int]) -> bool:
    try:
        CUR.execute("DELETE FROM Files WHERE FileID IN ({param})".format(
            param=','.join(['?']*len(fid))), tuple(fid))
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL filetags_clear_select Error\nERR: {err}")
        return False


def tags_get() -> List[Tuple[int, str, int]]:
    try:
        return list(CUR.execute('SELECT TagID, Tag, TagAdded FROM Tags ORDER BY TagAdded DESC'))
    except sqlite3.Error as err:
        print(f"SQL tags_get Error\nERR: {err}")
        return []


def filetags_clear() -> bool:
    "Entfernt alle nicht als Manuell markierten FileTag Einträge"
    try:
        CUR.execute("DELETE FROM FileTags WHERE Manual = ?", (False, ))
        CUR.execute("UPDATE Files SET LastIndexed = ?", (0, ))
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL filetags_clear Error\nERR: {err}")
        return False

def filetags_clear_select(fid: List[int]) -> bool:
    try:
        CUR.execute("DELETE FROM FileTags WHERE Manual = ? AND Part NOT NULL AND FileID in ({param})".format(
            param=','.join(['?']*len(fid))), (False, ) + tuple(fid))
        CUR.execute("UPDATE Files Set LastIndexed = ? WHERE FileID in ({param})".format(
            param=','.join(['?']*len(fid))), (0, ) + tuple(fid))
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL filetags_clear Error\nERR: {err}")
        return False


def filetags_add(fid: int, tags: List[Tuple[int, int, Optional[int], int, bool]]) -> bool:
    try:
        CUR.executemany("INSERT INTO FileTags (FileID, TagID, Part, Priority, Manual) VALUES (?, ?, ?, ?, ?)", tags)
        CUR.execute("UPDATE Files SET LastIndexed = strftime('%s', 'now') WHERE FileID = ?", (fid, ))
        CON.commit()
        return True
    except sqlite3.Error as err:
        print(f"SQL filetags_add Error\nERR: {err}")
        return False


def filetags_get(ftid: List[int]) -> List[Tuple[int, str]]:
    """
    INPUT: Liste an TagID Werten
    OUTPUT: Liste von Tuples mit Erstellungstimestamp und Tagnamen
    """
    try:
        return list(CUR.execute("SELECT Part, Tag FROM FileTags INNER JOIN Tags USING (TagID) WHERE FileTagID in ({param})".format(
            param=','.join(['?']*len(ftid))), tuple(ftid)))
    except sqlite3.Error as err:
        print(f"SQL filetags_get Error\nERR: {err}")
        return []


def search(tlist: List[str]) -> List[Tuple[str, int, int, List[int], int]]:
    """
    Nimmt eine Liste an Tags und gibt eine Liste an Konstruktorvariablen für FILE Objekte zurück.
    """
    try:
        query = CUR.execute("SELECT * FROM (SELECT FilePath, Files.FileID, LastIndexed, GROUP_CONCAT(DISTINCT Tag) AS CTag, GROUP_CONCAT(FileTagID), SUM(Priority) AS Prio FROM Files INNER JOIN FileTags USING (FileID) INNER JOIN Tags USING (TagID) WHERE {param} GROUP BY FilePath ORDER BY Prio DESC) WHERE length(CTag) = ?;".format(
            param=' OR '.join(["Tag LIKE ?"]*len(tlist))), (*tlist, len(','.join(tlist))))
        return [(x[0], x[1], x[2], list([int(y) for y in x[4].split(',')]), x[5]) for x in query]
    except sqlite3.Error as err:
        print(f"SQL search Error\nERR: {err}")
        return []


def dbexit() -> bool:
    "Datenbank cleanup"
    try:
        CON.commit()
        CON.close()
        return True
    except sqlite3.Error as err:
        print(f"SQL database cleanup error\nERR: {err}")
        return False


def __db_init__() -> bool:
    "Initialisiert die Datenbank"
    try:
        ktables = [x[0] for x in CUR.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
        if not all([x in ktables for x in ["Files", "Tags", "FileTags"]]):
            with open("database_schema.sql", 'r') as f:
                CUR.executescript(f.read())
        return True
    except sqlite3.Error as err:
        print(f"SQL database initialization error\nERR: {err}")
        return False


__db_init__()
atexit.register(dbexit)
