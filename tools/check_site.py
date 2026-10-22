#!/usr/bin/env python3
"""Contrôles du site avant commit : détecte les pages retirées ou vidées par erreur (par exemple par une régénération).

Usage :
  python3 tools/check_site.py                  contrôle (code de sortie 1 s'il y a un problème)
  python3 tools/check_site.py --update         ajoute au registre les nouvelles pages et relève la taille de celles qui ont grandi
  python3 tools/check_site.py --retirer CHEMIN retire VOLONTAIREMENT une page du registre (ex. posts/2026-10-16-xxx.html)
  python3 tools/check_site.py --accepter CHEMIN accepte VOLONTAIREMENT qu'une page soit devenue plus courte

Le registre tools/pages_attendues.tsv liste chaque page publiée (chemin, taille). Contrôles :
1. chaque page du registre existe encore, et n'a pas perdu plus de 40 % de sa taille (texte effacé) ;
2. tous les liens et images internes des pages pointent vers un fichier qui existe ;
3. toutes les adresses du plan du site existent ;
4. les textes rédigés à la main (tools/event_texts.json) sont bien présents dans leur page ;
5. chaque vidéo de tools/videos.json est sur la page Vidéos, avec sa vignette.
Une retrait voulu s'enregistre avec --retirer : sans cela, supprimer une page fait échouer le contrôle.
"""
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
REGISTRE = ROOT / "tools" / "pages_attendues.tsv"
MIN_RATIO = 0.6


def pages():
    """Pages publiées : racine, posts/, histoire/ et pages à la racine d'un dossier (hors redirections générées)."""
    found = {p for p in ROOT.glob("*.html")}
    found |= set((ROOT / "posts").glob("*.html"))
    found |= set((ROOT / "histoire").glob("**/index.html"))
    for name in ("mentions-legales", "reglement-interieur", "activites", "activites-2025-26", "activites-2024-25"):
        if (ROOT / name / "index.html").exists():
            found.add(ROOT / name / "index.html")
    return {str(p.relative_to(ROOT)): p.stat().st_size for p in found}


def lire_registre():
    reg = {}
    if REGISTRE.exists():
        for line in REGISTRE.read_text().splitlines():
            if line.strip():
                path, size = line.split("\t")
                reg[path] = int(size)
    return reg


def ecrire_registre(reg):
    REGISTRE.write_text("".join(f"{p}\t{s}\n" for p, s in sorted(reg.items())))


def cible(page, ref):
    """Fichier visé par un lien relatif depuis `page` (None si lien externe ou ancre)."""
    u = urlparse(html.unescape(ref))
    if u.scheme or u.netloc or not u.path or ref.startswith(("mailto:", "tel:", "#", "data:")):
        return None
    base = ROOT if u.path.startswith("/") else page.parent
    t = (base / unquote(u.path).lstrip("/")).resolve()
    return t / "index.html" if t.is_dir() else t


def controles():
    errs = []
    reg = lire_registre()
    actuelles = pages()
    # 1. pages disparues ou vidées
    for path, size in sorted(reg.items()):
        if path not in actuelles:
            errs.append(f"page supprimée : {path} (si c'est voulu : python3 tools/check_site.py --retirer {path})")
        elif actuelles[path] < size * MIN_RATIO:
            errs.append(f"page beaucoup plus courte ({size} -> {actuelles[path]} octets) : {path} "
                        f"(si c'est voulu : python3 tools/check_site.py --accepter {path})")
    # 2. liens et images internes
    for path in actuelles:
        page = ROOT / path
        text = page.read_text()
        for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
            t = cible(page, ref)
            if t is not None and not t.exists():
                errs.append(f"lien cassé dans {path} : {ref}")
        m = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', text)
        if m and (cible(page, m.group(1)) or ROOT).exists() is False:
            errs.append(f"redirection cassée dans {path} : {m.group(1)}")
    # redirections générées (anciennes adresses WordPress)
    for stub in ROOT.glob("**/index.html"):
        rel = stub.relative_to(ROOT)
        if str(rel) in actuelles or rel.parts[0] in ("tools", "images", "fonts", "js", "posts", "histoire"):
            continue
        m = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', stub.read_text())
        if m and not (cible(stub, m.group(1)) or ROOT).exists():
            errs.append(f"redirection cassée : {rel} -> {m.group(1)}")
    # 3. plan du site
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        site = "https://lespiedsontdesoreilles.fr/"
        for loc in re.findall(r"<loc>([^<]+)</loc>", sm.read_text()):
            rel = loc[len(site):] if loc.startswith(site) else loc
            t = ROOT / rel
            if rel == "":
                t = ROOT / "index.html"
            elif t.is_dir() or rel.endswith("/"):
                t = t / "index.html"
            if not t.exists():
                errs.append(f"adresse du plan du site introuvable : {loc}")
    # 4. textes rédigés à la main
    tf = ROOT / "tools" / "event_texts.json"
    if tf.exists():
        for slug, frag in json.loads(tf.read_text()).items():
            page = ROOT / "posts" / f"{slug}.html"
            if not page.exists():
                errs.append(f"page du texte rédigé à la main absente : posts/{slug}.html")
            elif frag[:120] not in page.read_text():
                errs.append(f"texte rédigé à la main absent de posts/{slug}.html (tools/event_texts.json)")
    # 5. vidéos
    vf, vp = ROOT / "tools" / "videos.json", ROOT / "videos.html"
    if vf.exists() and vp.exists():
        vtext = vp.read_text()
        for rule in json.loads(vf.read_text()):
            for vid, _ in rule["videos"]:
                if f'data-id="{vid}"' not in vtext:
                    errs.append(f"vidéo absente de videos.html : {vid} ({rule['date']} {rule['kw']})")
                elif not (ROOT / "images" / "videos" / f"{vid}.jpg").exists():
                    errs.append(f"vignette manquante : images/videos/{vid}.jpg")
    return errs


def main(argv):
    reg = lire_registre()
    if argv[:1] == ["--retirer"] and len(argv) == 2:
        if reg.pop(argv[1], None) is None:
            sys.exit(f"{argv[1]} n'est pas dans le registre")
        ecrire_registre(reg)
        print("retiré du registre :", argv[1])
        return 0
    if argv[:1] == ["--accepter"] and len(argv) == 2:
        reg[argv[1]] = (ROOT / argv[1]).stat().st_size
        ecrire_registre(reg)
        print("taille acceptée :", argv[1])
        return 0
    if argv[:1] == ["--update"]:
        actuelles = pages()
        n = 0
        for p, s in actuelles.items():
            if p not in reg or s > reg[p]:
                n += p not in reg
                reg[p] = s
        ecrire_registre(reg)
        print(f"registre mis à jour : {n} nouvelles pages, {len(reg)} au total")
        return 0
    errs = controles()
    if errs:
        print(f"{len(errs)} problème(s) :")
        for e in errs[:60]:
            print("  -", e)
        if len(errs) > 60:
            print(f"  … et {len(errs) - 60} autres")
        return 1
    print(f"site OK : {len(lire_registre())} pages suivies, liens, plan du site, textes rédigés à la main et vidéos vérifiés")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
