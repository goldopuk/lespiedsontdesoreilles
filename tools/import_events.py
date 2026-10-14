#!/usr/bin/env python3
"""Importe les affiches d'événements du disque dur (liste validée dans tools/events_curated.json).

Usage : python3 tools/import_events.py "<dossier racine du disque dur>"
- redimensionne chaque affiche (1000 px max) dans images/affiches/
- écrit tools/events.json, lu ensuite par tools/build_news.py
Seule l'affiche choisie est copiée : aucun document administratif n'est publié.
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images" / "affiches"


def slugify(t):
    nfkd = unicodedata.normalize("NFKD", t)
    s = "".join(c if ord(c) < 128 else ("" if unicodedata.combining(c) else " ") for c in nfkd)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50].strip("-")


def main(disk):
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    curated = json.loads((ROOT / "tools" / "events_curated.json").read_text())
    events, seen = [], set()
    for e in curated:
        slug = f'{e["date"]}-{slugify(e["title"])}'
        while slug in seen:
            slug += "-2"
        seen.add(slug)
        dest = IMG_DIR / f"evt-{slug}.jpg"
        if not dest.exists():
            subprocess.run(["magick", f'{Path(disk) / e["source"]}[0]', "-auto-orient", "-background", "white",
                            "-flatten", "-resize", "1000x1000>", "-quality", "82", str(dest)], check=True)
        events.append({"title": e["title"], "date": e["date"], "slug": slug, "poster": dest.name})
    (ROOT / "tools" / "events.json").write_text(json.dumps(events, ensure_ascii=False, indent=1))
    print(len(events), "affiches importées")


if __name__ == "__main__":
    main(sys.argv[1])
