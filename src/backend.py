from fileutils import FILE, DIRIN, DIROUT, search_files, clear, copy, exists_not
import database
import extractor
from typing import List, Tuple

def __tags_init__() -> bool:
    "Fügt alle Tags aus ../Suchbegriffe.txt zur Datenbank hinzu"
    try:
        tdb = [x[1] for x in database.tags_get()]
        new = [t.replace("\n", "") for t in open("../Suchbegriffe.txt", 'r', encoding="utf-8") if t.replace("\n", "") not in tdb]
        print(f"New Tags: {new}")
        return all([database.tag_add(tag) for tag in new])
    except OSError as err:
        print(f"Failed reading tag init file\nERR: {err}")
        return False


def update(full_scan: bool) -> bool:
    if (full_scan and database.files_clear()) or True:
        # Füge neue Dateien dazu und markiere veränderte Dateien zur Indexierung
        dfile = {x[0]: FILE(*x) for x in database.files_get()}
        tags = database.tags_get()
        files_clear = []
        files_add = []
        for f in search_files([DIRIN]):
            if f[0] not in dfile.keys():
                files_add.append(f[0])
            elif f[1] > dfile[f[0]].mtime:
                files_clear.append(dfile[f[0]].id)
        database.filetags_clear_select(files_clear)
        database.files_add([(f, 0) for f in files_add])
        database.files_clear_select([dfile[p].id for p in exists_not(list(dfile.keys()))])
        # Durchsuche zu Indexierende Dateien
        for fdue in [FILE(*x) for x in database.files_get_due()]:
            ftags = extractor.search_tags(
                extractor.get_text(fdue),
                tags_check(fdue, tags)
            )
            database.filetags_add(
                fdue.id, [(fdue.id, tag[1], tag[0], 3, False) for tag in ftags]
            )
            if fdue.__repr__() in files_add:
                ntags = extractor.search_tags(
                    [fdue.__repr__()],
                    tags
                )
                database.filetags_add(
                    fdue.id, [(fdue.id, tag[1], None, 10, False) for tag in ntags]
                )
        return True
    else:
        print("ERR: Update failed.\nValue of full_scan: {full_scan}")
        return False


def search(stags: List[str]) -> List[FILE]:
    query = database.search(stags)
    files = [FILE(*x[0:3], database.filetags_get(x[3]), x[4]) for x in query]
    return files


def get_documents(fid: List[int], rm: bool) -> bool:
    if rm:
        clear()
    return all([copy(f[0]) for f in database.files_get_select(fid)])

def tags_check(f: FILE, tags: List[Tuple[int, str, int]]) -> List[Tuple[int, str, int]]:
    tags_match: List[Tuple[int, str, int]] = []
    for t in tags:
        if t[2] > f.mtime:
            tags_match.append(t)
            continue
        break
    return tags_match

__tags_init__()
