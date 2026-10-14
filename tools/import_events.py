#!/usr/bin/env python3
"""Importe les événements d'archives : affiches du disque dur + informations de la page Facebook.

Usage : python3 tools/import_events.py "<dossier racine du disque dur>"
Sources :
- tools/events_curated.json  : affiches du disque dur validées (titre + mois, pour les événements sans fiche Facebook)
- tools/events_fb_data.py    : événements et séries lus sur Facebook (date exacte, lieu, texte)
- tools/events_scan.json     : inventaire des dossiers du disque dur (chemins des affiches)
Écrit images/affiches/evt-*.jpg (1000 px max) et tools/events.json, lu par tools/build_news.py.
Seule l'affiche choisie est copiée : aucun document administratif n'est publié.
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import events_fb_data as fb  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images" / "affiches"
# affiches de remplacement quand le choix automatique était une image libre de droits
OVR = {8: "2021/202107 forro na chuva à l'appart/banner.jpg",
       30: "2022/202211 jam session atelier avec Aline et alise et Gabriel/jam session aline.jpg",
       32: "2023/202301 brunch et ateliers gabriel/brunch dimanche 8 janv.jpg",
       34: "2023/202302 saira et stages/saira carnaval.jpg",
       28: "2022/202209 rentrée/banniere FB Porte ouverte cours musique forro.jpg"}


def slugify(t):
    nfkd = unicodedata.normalize("NFKD", t)
    s = "".join(c if ord(c) < 128 else ("" if unicodedata.combining(c) else " ") for c in nfkd)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50].strip("-")


def main(disk):
    disk = Path(disk)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    scan = json.loads((ROOT / "tools" / "events_scan.json").read_text())

    def poster_path(idx):
        return OVR.get(idx) or scan[idx]["poster"]

    def convert(src, slug):
        dest = IMG_DIR / f"evt-{slug}.jpg"
        if not dest.exists():
            subprocess.run(["magick", f"{disk / src}[0]", "-auto-orient", "-background", "white", "-flatten",
                            "-resize", "1000x1000>", "-quality", "82", str(dest)], check=True)
        return dest.name

    out, seen, used = [], set(), set()

    def unique(slug):
        while slug in seen:
            slug += "-2"
        seen.add(slug)
        return slug

    for e in fb.EVENTS:
        slug = unique(f'{e["date"]}-{slugify(e["title"])}')
        poster = None
        if e["poster"] is not None:
            used.add(poster_path(e["poster"]))
            poster = convert(poster_path(e["poster"]), slug)
        out.append({"kind": "event", "slug": slug, "title": e["title"], "date": e["date"], "end": e["end"], "place": e["place"],
                    "desc": e["desc"], "also": e["also"], "other_org": e["other_org"], "poster": poster})

    for s in fb.SERIES:
        slug = unique(f'{s["date"]}-{s["slug"]}')
        poster = None
        if s["poster"] is not None:
            used.add(poster_path(s["poster"]))
            poster = convert(poster_path(s["poster"]), slug)
        out.append({"kind": "series", "slug": slug, "title": s["title"], "date": s["date"] + "-01" if len(s["date"]) == 7 else s["date"],
                    "intro": s["intro"], "dates": s["dates"], "poster": poster})

    used |= {poster_path(i) for i in fb.DROP_POSTERS}
    # affiches du disque dur sans fiche Facebook : on garde titre + mois
    for e in json.loads((ROOT / "tools" / "events_curated.json").read_text()):
        if e["source"] in used:
            continue
        slug = unique(f'{e["date"]}-{slugify(e["title"])}')
        out.append({"kind": "archive", "slug": slug, "title": e["title"], "date": e["date"] + "-01", "month": True,
                    "poster": convert(e["source"], slug)})

    (ROOT / "tools" / "events.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    kinds = {k: sum(1 for x in out if x["kind"] == k) for k in ("event", "series", "archive")}
    print(kinds)


if __name__ == "__main__":
    main(sys.argv[1])
