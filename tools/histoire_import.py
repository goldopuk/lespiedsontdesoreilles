#!/usr/bin/env python3
"""Prépare les textes de « Notre histoire » à partir des brouillons hors dépôt.

Usage : python3 tools/histoire_import.py "<dossier chronologie>"
Lit histoire_courte.md et par_annee/*.md, retire tout ce qui ne doit pas être public (section « À vérifier »,
montants de comptabilité, remboursements de la sono, commissions, tarifs, notes de rédaction) et écrit des copies
propres dans tools/histoire/. Ces copies sont publiques (dépôt GitHub) : ne rien y mettre d'interne.
"""
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "histoire"

# retraits dans le récit : (texte brut, remplacement). Chaque motif doit être trouvé, sinon le brouillon a changé.
EDITS = {
    "2020-21": [(" (375 € récoltés début juin)", ""), (", pour 555 €", ""),
                ("cagnotte pour l'enceinte (375 €), achat d'une JBL", "cagnotte pour l'enceinte, achat d'une JBL")],
    "2021-22": [(", pour environ 850 € d'investissement", "")],
    "2023-24": [(" (3 954 €, dont Julien avance 3 400 €, le temps que l'association rembourse)", "")],
    "2024-25": [(", et nous commençons à rembourser la sono.", "."),
                (" Le 8 novembre, Julien commence à être remboursé de la sono: 900 €, une bonne nouvelle pour son compte en banque.", ""),
                (" (763 €, dont nous ne regrettons pas un centime)", " (dont nous ne regrettons pas un centime)")],
    "2025-26": [(" et d'une publicité sur Facebook: 55 €, le prix d'un bon bal, avec nettement moins de monde dans la salle", ""),
                (" (828 €)", ""),
                ("Le 5 mai, Julien reçoit un deuxième remboursement de 900 € pour la sono. ", "")],
}
# lignes d'« Activités hebdomadaires » à retirer
DROP_LINES = {"2023-24": ["Pour ces cours, l'association prélève"], "2025-26": ["Tarifs:"]}
# « Chiffres » publics : effectifs approximatifs seulement
CHIFFRES = {
    "2019-20": "Fréquentation du dimanche à L'Appart : 15 à 30 personnes en général.",
    "2021-22": "23 adhérents en danse.",
    "2022-23": "35 adhérents en danse (21 en niveau 1, 14 en niveau 2) et 14 en musique, soit environ 45 adultes (4 font danse et musique).",
    "2023-24": "43 adhérents en danse, 6 en musique adultes et 21 enfants, soit environ 46 adultes (3 font danse et musique).",
    "2024-25": "36 adhérents en danse et 8 en musique, soit 41 adultes distincts.",
    "2025-26": "34 adhérents en danse (niveau 1 : 15, niveau 2 : 12, niveau 3 : 7), 7 en musique et 3 adhérents sans cours, soit 41 membres.",
}
KEEP = ("En deux phrases", "Le récit", "Activités hebdomadaires", "Dates marquantes")


def sections(text):
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return parts[0], dict(zip(parts[1::2], parts[2::2]))


def draft_note(head):
    return re.sub(r"^\(.*?\)\s*$", "", head, flags=re.M)


def main(src):
    src = Path(src)
    OUT.mkdir(exist_ok=True)
    head, _ = sections((src / "histoire_courte.md").read_text())
    # le texte validé s'arrête avant « À vérifier avant publication »
    story = head.split("\n", 1)[1]
    story = draft_note(story).strip()
    (OUT / "histoire_courte.md").write_text(head.split("\n", 1)[0] + "\n\n" + story + "\n")
    for f in sorted((src / "par_annee").glob("*.md")):
        season = f.stem
        head, secs = sections(f.read_text())
        title = head.strip().splitlines()[0]
        out = [title, ""]
        for name in KEEP:
            txt = secs[name].strip()
            for old, new in EDITS.get(season, []):
                if old in txt:
                    txt = txt.replace(old, new)
            lines = [l for l in txt.splitlines()
                     if not any(l.lstrip("- ").startswith(d) for d in DROP_LINES.get(season, []))]
            out += [f"## {name}", "", "\n".join(lines).strip(), ""]
        if season in CHIFFRES:
            out += ["## Chiffres", "", f"- {CHIFFRES[season]}", ""]
        text = "\n".join(out)
        for old, new in EDITS.get(season, []):
            assert old not in text, (season, old)
        assert not re.search(r"€|commission|remboursé|usage interne|À vérifier", text), (season, re.findall(r".{20}(?:€|commission|rembours|usage interne).{10}", text))
        (OUT / f"{season}.md").write_text(text)
    print("copies propres écrites dans", OUT)


if __name__ == "__main__":
    main(sys.argv[1])
