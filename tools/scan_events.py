#!/usr/bin/env python3
"""Inventaire des dossiers d'événements du disque dur : date, titre, affiche candidate.

Usage : python3 tools/scan_events.py "<dossier racine>" <sortie.json>
Ne lit que les noms de fichiers ; rien n'est copié ni publié.
"""
import json
import os
import re
import sys

IMG = (".jpg", ".jpeg", ".png", ".webp")
GOOD = {"affiche": 5, "fb": 4, "facebook": 4, "flyer": 3, "event": 2, "evenement": 2, "save": 1}
BAD = {"insta": -5, "instagram": -5, "story": -5, "stories": -5, "banniere": -5, "banner": -5, "hello": -5,
       "planning": -5, "print": -5, "logo": -5, "admin": -9, "qr": -5, "attestation": -9, "recapitulatif": -9,
       "benevoles": -4, "bénévoles": -4, "sd": -1, "nb": -2, "psd": -9}


def score(name):
    low = os.path.splitext(name)[0].lower()
    tokens = re.split(r"[^a-zàâçéèêëîïôûùüÿ0-9]+", low)
    s = sum(GOOD.get(t, 0) + BAD.get(t, 0) for t in tokens)
    if re.match(r"^(img|dsc|photo|p\d|\d+)", low):
        s -= 3  # probablement une photo
    return s


def parse(folder):
    m = re.match(r"^(\d{4})(\d{2})(\d{2})?\s*[-–]?\s*(.*)$", folder)
    if not m:
        return None
    y, mo, d, title = m.groups()
    title = re.sub(r"\s+", " ", title).strip(" -–")
    return {"date": f"{y}-{mo}-{d or '01'}", "precision": "day" if d else "month", "title": title[:1].upper() + title[1:]}


def main(root, out):
    events = []
    for y in sorted(os.listdir(root)):
        p = os.path.join(root, y)
        if re.match(r"^20\d\d$", y) and os.path.isdir(p):
            dirs = [os.path.join(p, e) for e in sorted(os.listdir(p))]
        elif re.match(r"^20\d{6} ", y) and os.path.isdir(p):
            dirs = [p]
        else:
            continue
        for d in dirs:
            if not os.path.isdir(d):
                continue
            info = parse(os.path.basename(d))
            if not info:
                continue
            files = []
            for dp, dn, fn in os.walk(d):
                depth = dp[len(d):].count(os.sep)
                dn[:] = [x for x in dn if x.lower() not in ("admin", "print", "csv", "old")] if depth < 1 else []
                if depth == 1 and os.path.basename(dp).lower() not in ("fb", "facebook"):
                    continue
                files += [os.path.join(dp, f) for f in fn if f.lower().endswith(IMG)]
            files.sort(key=lambda f: (-score(os.path.basename(f)), -os.path.getsize(f)))
            info.update(folder=os.path.relpath(d, root), poster=files[0] if files else None,
                        others=[os.path.relpath(f, root) for f in files[1:4]], nimages=len(files))
            if info["poster"]:
                info["poster"] = os.path.relpath(info["poster"], root)
            events.append(info)
    json.dump(events, open(out, "w"), ensure_ascii=False, indent=1)
    print(len(events), "dossiers,", sum(1 for e in events if not e["poster"]), "sans image")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
