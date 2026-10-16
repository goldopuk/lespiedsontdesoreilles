#!/usr/bin/env python3
"""Génère les pages « statiques » de l'ancien site et les redirections des anciennes adresses.

Usage : python3 tools/build_pages.py   (après tools/build_news.py)
- <slug>/index.html pour les pages reprises (règlement, mentions légales, anciennes saisons)
- une page de redirection (meta refresh) pour chaque ancienne adresse WordPress,
  car GitHub Pages ne gère pas de redirections côté serveur
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_news as bn  # noqa: E402

ROOT = bn.ROOT
SITE = "https://lespiedsontdesoreilles.fr"

# pages reprises telles quelles : slug -> titre affiché
KEPT = {
    "reglement-interieur": "Règlement intérieur",
    "mentions-legales": "Mentions légales",
    "activites-2025-26": "Activités 2025-26",
    "activites-2024-25": "Activités 2024-25",
    "activites": "Activités 2023-24",
}
# anciennes pages remplacées par une section de l'accueil ou une autre page
REDIRECTS = {
    "about": "index.html#asso",
    "actualites": "actualites.html",
    "activites-2026-27": "index.html#activites",
    "newsletter": "index.html#contact",
    "le-forro": "index.html#forro",
    "les-liens": "index.html#liens",
    "contact": "index.html#contact",
}
# corrections nécessaires depuis le changement d'hébergement
MENTIONS_FIXES = [
    ("https://lespiedsontdesoreilles.wordpress.com/", SITE + "/"),
    ("Hébergeur du site web: wordpress.com",
     "Hébergeur du site web : GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis"),
]


def redirect_page(target, prefix):
    url = f"{prefix}{target}"
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8">'
            f'<title>Redirection…</title><meta name="robots" content="noindex">'
            f'<link rel="canonical" href="{SITE}/{target}">'
            f'<meta http-equiv="refresh" content="0; url={url}">'
            f'<script>location.replace({json.dumps(url)})</script></head>'
            f'<body><p>Cette page a déménagé : <a href="{url}">cliquez ici</a>.</p></body></html>\n')


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    pages = {p["slug"]: p for p in json.loads((ROOT / "tools" / "pages.json").read_text())["posts"]}
    posts = [p for p in json.loads((ROOT / "tools" / "posts.json").read_text())["posts"] if p["slug"] != "contact"]

    for slug, title in KEPT.items():
        content = pages[slug]["content"]
        if slug == "mentions-legales":
            for old, new in MENTIONS_FIXES:
                content = content.replace(old, new)
        body = bn.convert_content(content, "../")
        body = (f'<article class="post"><p><a href="../index.html">← Accueil</a></p>'
                f'<h1>{html.escape(title)}</h1><div class="post-body">{body}</div></article>')
        write(ROOT / slug / "index.html", bn.page(title, body, "../"))

    for slug, target in REDIRECTS.items():
        write(ROOT / slug / "index.html", redirect_page(target, "../"))

    # anciennes adresses des articles : /AAAA/MM/JJ/slug/ -> posts/<nouveau-slug>.html
    seen = set()
    for p in sorted(posts, key=lambda p: p["date"], reverse=True):
        slug = bn.make_slug(p["title"], p["date"])
        while slug in seen:
            slug += "-2"
        seen.add(slug)
        y, m, d = p["date"][:10].split("-")
        target = "actualites.html" if p["slug"] in bn.EXCLUDED else f"posts/{slug}.html"
        write(ROOT / y / m / d / p["slug"] / "index.html", redirect_page(target, "../../../../"))
        # certaines annonces existaient aussi comme page à la racine (/slug/)
        if p["slug"] in pages and p["slug"] not in KEPT and p["slug"] not in REDIRECTS:
            write(ROOT / p["slug"] / "index.html", redirect_page(f"posts/{slug}.html", "../"))

    write(ROOT / ".nojekyll", "")
    # plan du site et robots.txt (adresses du domaine définitif)
    urls = ["", "actualites.html"] + [f"{s}/" for s in KEPT] + sorted(
        f"posts/{f.name}" for f in (ROOT / "posts").glob("*.html"))
    sm = "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls)
    write(ROOT / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    write(ROOT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    write(ROOT / "404.html", bn.page("Page introuvable",
          '<section><h1>Page introuvable</h1><p>Cette page n\'existe pas ou a changé d\'adresse.</p>'
          '<p><a class="button" href="/index.html">Retour à l\'accueil</a> '
          '<a class="button" href="/actualites.html">Les actualités</a></p></section>', "/"))
    print("pages et redirections générées")


if __name__ == "__main__":
    main()
