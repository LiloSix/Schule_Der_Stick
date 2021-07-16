from typing import List, Tuple
import PyPDF2
from fileutils import FILE


def __get_pdf(fpath: str) -> List[str]:
    "Extrahiert Text aus PDF Dateien"
    try:
        txt = ""
        f = PyPDF2.PdfFileReader(fpath, strict=False)
        for page in [f.getPage(x) for x in range(f.getNumPages())]:
            txt += page.extractText().replace("\n", " ")
        return txt.split(". ")
    except Exception as e:
        print(f"Exception while trying to read {fpath}\nERR: {e}\n\n")
        return []

def __get_docx(fpath: str) -> List[str]:
    return []

def __get_pptx(fpath: str) -> List[str]:
    return []

def __get_txt(fpath: str) -> List[str]:
    try:
        return [x for x in open(fpath, 'r', encoding="utf-8")]
    except Exception as e:
        print(f"Exception while trying to read {fpath}\nERR: {e}\n")
        return []

def get_text(f: FILE) -> List[str]:
    """
    Meta Funktion, leitet je nach Dateiendung den Dateipfad an die entsprechende get Funktion.
    """
    if f.type == ".pdf":
        return __get_pdf(f.full_path())
    elif f.type in [".doc", ".docx"]:
        return __get_docx(f.full_path())
    if f.type == ".pptx":
        return __get_pptx(f.full_path())
    if f.type == ".txt":
        return __get_txt(f.full_path())
    else:
        return []


def search_tags(text: List[str], tags: List[Tuple[int, str, int]]) -> List[Tuple[int, int]]:
    matches = []
    for i, txt in enumerate(text):
        for tag in tags:
            if tag[1] in txt:
                matches.append((i, tag[0]))
    return matches
