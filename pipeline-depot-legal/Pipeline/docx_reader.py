"""Lecture du fichier .docx : extraction des paragraphes avec mise en forme (gras, puces).

Usage :
    python docx_reader.py [chemin.docx]      # affiche le détail des paragraphes
"""
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

from chemins import DOCX_ORIGINAL, DOCX_SOURCE_COPY

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# Emplacement par défaut : d'abord la copie locale sous Dependence_Pipeline, sinon l'original
DEFAULT_DOCX = (
    str(DOCX_SOURCE_COPY) if DOCX_SOURCE_COPY.exists() else str(DOCX_ORIGINAL)
)


def paragraph_text(p) -> str:
    parts = []
    for node in p.iter():
        if node.tag == f"{W}t":
            parts.append(node.text or "")
        elif node.tag in (f"{W}tab",):
            parts.append("\t")
        elif node.tag == f"{W}br":
            parts.append("\n")
    return "".join(parts)


def paragraph_flags(p) -> dict:
    runs = p.findall("w:r", NS)
    bold_runs = 0
    total_runs = 0
    for r in runs:
        rpr = r.find("w:rPr", NS)
        is_bold = rpr is not None and rpr.find("w:b", NS) is not None
        total_runs += 1
        if is_bold:
            bold_runs += 1
    numpr = p.find("w:pPr/w:numPr", NS)
    return {
        "bold": total_runs > 0 and bold_runs == total_runs,
        "bullet": numpr is not None,
    }


def read_paragraphs(path: str) -> list[dict]:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find("w:body", NS)
    out = []
    idx = 0
    for p in body.iter(f"{W}p"):
        text = paragraph_text(p).strip()
        if not text:
            continue
        idx += 1
        flags = paragraph_flags(p)
        out.append({"i": idx, "text": text, **flags})
    return out


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOCX
    for p in read_paragraphs(path):
        marks = []
        if p["bold"]:
            marks.append("GRAS")
        if p["bullet"]:
            marks.append("PUCES")
        label = ",".join(marks) or "     "
        print(f"{p['i']:3d} [{label:9s}] {p['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
