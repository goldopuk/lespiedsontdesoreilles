#!/usr/bin/env python3
"""Génère la page « Notre histoire » (histoire/index.html) et une page par saison (histoire/<saison>/index.html).

Usage : python3 tools/build_histoire.py
Lit les textes propres de tools/histoire/ (voir tools/histoire_import.py) et utilise le gabarit page() de build_news.py.
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_news as bn  # noqa: E402

ROOT = bn.ROOT
SRC = Path(__file__).resolve().parent / "histoire"


def md(text):
    """Markdown minimal : titres ##, listes à puces, paragraphes."""
    out, items = [], []

    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
            items.clear()

    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if lines[0].startswith("## "):
            flush()
            out.append(f"<h2>{html.escape(lines[0][3:])}</h2>")
            lines = lines[1:]
        if lines and all(l.startswith("- ") for l in lines):
            items.extend(html.escape(l[2:]) for l in lines)
            flush()
        elif lines:
            flush()
            out.append(f"<p>{html.escape(' '.join(lines))}</p>")
    flush()
    return "\n".join(out)


def split(text):
    """(titre, {section: texte}) d'un fichier de saison."""
    title = text.splitlines()[0].lstrip("# ").strip()
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return title, dict(zip(parts[1::2], (p.strip() for p in parts[2::2])))


def noel_posts(season):
    """Articles « Jam de Noël » de la saison (septembre à août), pour la rubrique « Voir aussi »."""
    y = int(season[:4])
    found = []
    for f in sorted((ROOT / "posts").glob("*noel*.html")):
        d = f.name[:10]
        if f"{y}-09-01" <= d <= f"{y + 1}-08-31":
            h1 = re.search(r"<h1>(.*?)</h1>", f.read_text())
            found.append((f.name, h1.group(1) if h1 else f.stem))
    return found


def main():
    seasons = sorted(p.stem for p in SRC.glob("20*.md"))
    data = {s: split((SRC / f"{s}.md").read_text()) for s in seasons}

    for i, s in enumerate(seasons):
        title, secs = data[s]
        body = f'<p><a href="../">← Notre histoire</a></p><h1>{html.escape(title)}</h1>'
        body += f'<p class="lead">{html.escape(secs["En deux phrases"])}</p>'
        for name in ("Le récit", "Activités hebdomadaires", "Dates marquantes", "Chiffres"):
            if name in secs:
                body += md(f"## {name}\n\n{secs[name]}")
        extra = noel_posts(s)
        if extra:
            body += "<h2>Voir aussi</h2><ul>" + "".join(f'<li><a href="../../posts/{f}">{t}</a></li>' for f, t in extra) + "</ul>"
        prev_s = seasons[i - 1] if i else None
        next_s = seasons[i + 1] if i + 1 < len(seasons) else None
        nav = '<nav class="post-nav">'
        nav += f'<a href="../{prev_s}/">← Saison {prev_s}</a>' if prev_s else "<span></span>"
        nav += f'<a href="../{next_s}/">Saison {next_s} →</a>' if next_s else "<span></span>"
        nav += "</nav>"
        desc = secs["En deux phrases"]
        out = ROOT / "histoire" / s / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(bn.page(f"Saison {s}", f'<article class="post"><div class="post-body">{body}</div>{nav}</article>', "../../", desc))

    story = (SRC / "histoire_courte.md").read_text().split("\n", 1)
    body = f"<h1>{html.escape(story[0].lstrip('# ').strip())}</h1>" + md(story[1])
    body += "<h2>Saison par saison</h2><ul>"
    for s in seasons:
        title, secs = data[s]
        label = title.split(":", 1)[1].strip().capitalize() if ":" in title else title
        body += f'<li><a href="{s}/"><strong>{s}</strong> : {html.escape(label)}</a><br>{html.escape(secs["En deux phrases"])}</li>'
    body += "</ul>"
    out = ROOT / "histoire" / "index.html"
    out.write_text(bn.page("Notre histoire", f'<article class="post"><div class="post-body">{body}</div></article>', "../",
                           "L'histoire de l'association Les pieds ont des oreilles, de 2019 à aujourd'hui, saison par saison."))
    print(f"{len(seasons)} saisons + page Notre histoire générées")


if __name__ == "__main__":
    main()
