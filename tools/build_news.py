#!/usr/bin/env python3
"""Génère les pages d'actualités à partir de tools/posts.json (export de l'ancien site WordPress).

Usage : python3 tools/build_news.py
- télécharge les affiches dans images/affiches/ (une seule fois)
- écrit posts/*.html et actualites.html
- met à jour le bloc d'actualités de index.html (entre les marqueurs NEWS)
"""
import datetime
import html
import json
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images" / "affiches"
MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
          "septembre", "octobre", "novembre", "décembre"]
HOME_COUNT = 6
# articles WordPress retirés du site (événement annulé, etc.) : slug WordPress d'origine
EXCLUDED = {"electrofaune"}


def fr_date(iso):
    y, m, d = iso[:10].split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def shown_date(p):
    """Les événements importés du disque dur n'ont que le mois et l'année."""
    if p.get("month") or (p.get("event") or {}).get("kind") == "series":
        y, m = p["date"][:7].split("-")
        return f"{MONTHS[int(m) - 1]} {y}"
    return fr_date(p["date"])


def clean_title(t):
    t = html.unescape(t)
    # retire les emojis de début/fin pour garder un titre sobre
    t = re.sub(r"^[^\w«\"']+|[^\w»\"'.!?)]+$", "", t, flags=re.UNICODE)
    return t.strip() or html.unescape(t)


def make_slug(title, date):
    nfkd = unicodedata.normalize("NFKD", clean_title(title))
    # accents retirés, emojis et autres symboles remplacés par un espace (évite de coller les mots)
    s = "".join(c if ord(c) < 128 else ("" if unicodedata.combining(c) else " ") for c in nfkd)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60].strip("-")
    return f"{date[:10]}-{s or 'actu'}"


def local_name(url):
    """URL d'image WordPress -> nom de fichier local unique (année-mois-nom)."""
    path = url.split("?")[0]
    m = re.search(r"/uploads/(\d{4})/(\d{2})/(.+)$", path)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else Path(path).name


def download(url):
    name = local_name(url)
    dest = IMG_DIR / name
    if not dest.exists():
        src = url.split("?")[0]
        if re.search(r"\.(jpe?g|png)$", src, re.I):
            src += "?w=1000"  # redimensionné par WordPress : évite les fichiers énormes
        # curl plutôt qu'urllib : évite les soucis de certificats Python sur macOS
        r = subprocess.run(["curl", "-fsSL", "--max-time", "60", "-o", str(dest), src],
                           capture_output=True, text=True)
        if r.returncode != 0:  # image absente : on continue
            dest.unlink(missing_ok=True)
            print("  ! échec", url, r.stderr.strip())
            return None
    return name


UPLOAD_RE = re.compile(r"https?://[^\s\"'<>]*?/wp-content/uploads/[^\s\"'<>]+")


def convert_content(content, prefix):
    """Nettoie le HTML WordPress : images locales, emojis en texte, classes retirées."""
    def img(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        alt = alt.group(1) if alt else ""
        if not src or "/wp-content/uploads/" not in src.group(1):
            return alt  # emoji Facebook -> caractère
        name = download(src.group(1))
        return f'<img src="{prefix}images/affiches/{name}" alt="{alt}" loading="lazy">' if name else ""

    content = re.sub(r"<img[^>]*>", img, content)

    def link(m):  # liens vers les médias WordPress : on pointe vers la copie locale
        name = download(m.group(0))
        return f"{prefix}images/affiches/{name}" if name else m.group(0)

    content = UPLOAD_RE.sub(link, content)
    content = re.sub(r'\s(class|style|data-[\w-]+|srcset|sizes)="[^"]*"', "", content)
    return content


def poster_of(post):
    url = post.get("featured_image") or next((a["URL"] for a in post["attachments"].values()
                                              if a["mime_type"].startswith("image/")), None)
    if url:
        return download(url)
    imgs = re.findall(r'<img[^>]+src="([^"]*wp-content/uploads/[^"]+)"', post["content"])
    return download(imgs[0]) if imgs else None


def page(title, body, prefix, description="", body_class=""):
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} – Les pieds ont des oreilles</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="icon" href="{prefix}images/logo-podo.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap">
  <link rel="stylesheet" href="{prefix}style.css">
</head>
<body class="{body_class}">
  <header class="site-header">
    <a class="brand" href="{prefix}index.html">
      <img src="{prefix}images/logo-podo.jpg" alt="" width="55" height="60">
      <span>Les pieds ont des oreilles</span>
    </a>
    <nav>
      <a href="{prefix}index.html#asso">L'asso</a>
      <a href="{prefix}actualites.html">Actualités</a>
      <a href="{prefix}index.html#activites">Activités 2026-27</a>
      <a href="{prefix}index.html#forro">Le forró</a>
      <a href="{prefix}index.html#liens">Liens</a>
      <a href="{prefix}index.html#contact">Contact</a>
    </nav>
  </header>
  <main class="subpage">
{body}
  </main>
  <footer>
    <p>© 2026 Les pieds ont des oreilles ·
      <a href="{prefix}mentions-legales/">Mentions légales</a> ·
      <a href="{prefix}reglement-interieur/">Règlement intérieur</a></p>
  </footer>
</body>
</html>
"""


WEEKDAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month - 1]} {d.year}"


def render_event(e):
    """Texte d'un événement d'archive : (ligne de date, corps HTML)."""
    kind = e["kind"]
    if kind == "archive":
        y, m = e["date"][:7].split("-")
        return f"Événement de {MONTHS[int(m) - 1]} {y}", ""
    if kind == "series":
        items = "".join(f'<li><time datetime="{d}">{fr_date(d)}</time> : {html.escape(t)}</li>' for d, t in e["dates"])
        return "Rendez-vous réguliers", f'<p>{html.escape(e["intro"])}</p><ul>{items}</ul>'
    if e.get("end") and e["end"] != e["date"]:
        when = f'Du {long_date(e["date"])} au {long_date(e["end"])}'
    else:
        when = long_date(e["date"]).capitalize()
    parts = []
    if e.get("place"):
        parts.append(f'<p><strong>Lieu :</strong> {html.escape(e["place"])}</p>')
    parts += [f"<p>{html.escape(l)}</p>" for l in e.get("desc", "").split("\n") if l.strip()]
    if e.get("other_org"):
        parts.append(f'<p class="note">{html.escape(e["other_org"])}.</p>')
    if e.get("also"):
        items = "".join(f'<li>{fr_date(a["date"])} : {html.escape(a["title"])} ({html.escape(a["place"])})</li>' for a in e["also"])
        parts.append(f"<h2>Aussi au programme</h2><ul>{items}</ul>")
    return when, "".join(parts)


_RATIOS = {}


def poster_ratio(name):
    """Largeur / hauteur de l'affiche (mise en cache) ; permet d'adapter la vignette."""
    if name not in _RATIOS:
        r = subprocess.run(["magick", "identify", "-format", "%w %h", str(IMG_DIR / name) + "[0]"],
                           capture_output=True, text=True)
        try:
            w, h = map(int, r.stdout.split())
            _RATIOS[name] = w / h
        except ValueError:
            _RATIOS[name] = 1.91
    return _RATIOS[name]


def card(p, prefix):
    if p["poster"]:
        src = f'{prefix}images/affiches/{p["poster"]}'
        # seules les images au format exact des bannières Facebook (16:9) remplissent le cadre ; les autres s'affichent en entier sur fond flouté, sans rognage
        fit = abs(poster_ratio(p["poster"]) - 16 / 9) > 0.04
        thumb = (f'<div class="thumb{" fit" if fit else ""}" style="--bg:url(\'{src}\')">'
                 f'<img src="{src}" alt="Affiche : {html.escape(p["title"])}" loading="lazy"></div>')
    else:
        thumb = '<div class="thumb no-poster" aria-hidden="true"></div>'
    return (f'<a class="news-card" href="{prefix}posts/{p["slug"]}.html">{thumb}'
            f'<span class="news-title">{html.escape(p["title"])}</span>'
            f'<time datetime="{p["date"]}">{shown_date(p)}</time></a>')


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "posts").mkdir(exist_ok=True)
    for old in (ROOT / "posts").glob("*.html"):  # repart de zéro : évite les pages obsolètes
        old.unlink()
    raw = json.loads((ROOT / "tools" / "posts.json").read_text())["posts"]
    raw = [p for p in raw if p["slug"] != "contact" and p["slug"] not in EXCLUDED]  # la page contact est dans index.html
    raw.sort(key=lambda p: p["date"], reverse=True)

    posts, seen = [], set()
    for r in raw:
        title = clean_title(r["title"])
        slug = make_slug(r["title"], r["date"])
        while slug in seen:
            slug += "-2"
        seen.add(slug)
        print("•", slug)
        posts.append({"title": title, "slug": slug, "date": r["date"][:10], "raw": r,
                      "poster": poster_of(r)})

    # événements d'archives : fiches Facebook (texte, lieu), séries régulières, affiches seules
    events_file = ROOT / "tools" / "events.json"
    if events_file.exists():
        for e in json.loads(events_file.read_text()):
            posts.append({"title": e["title"], "slug": e["slug"], "date": e["date"], "month": e.get("month", False),
                          "raw": {"content": ""}, "poster": e["poster"], "event": e})
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)

    for i, p in enumerate(posts):
        if p.get("event"):
            heading_time, body_html = render_event(p["event"])
        else:
            body_html = convert_content(p["raw"]["content"], "../")
            heading_time = f'Publié le {shown_date(p)}'
        poster = ""
        # affiche en tête, sauf si le texte contient déjà la même image
        if p["poster"] and p["poster"] not in body_html:
            poster = f'<img class="poster" src="../images/affiches/{p["poster"]}" alt="Affiche : {html.escape(p["title"])}">'
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = '<nav class="post-nav">'
        nav += f'<a href="{older["slug"]}.html">← {html.escape(older["title"])}</a>' if older else "<span></span>"
        nav += f'<a href="{newer["slug"]}.html">{html.escape(newer["title"])} →</a>' if newer else "<span></span>"
        nav += "</nav>"
        body = (f'<article class="post"><p><a href="../actualites.html">← Toutes les actualités</a></p>'
                f'<h1>{html.escape(p["title"])}</h1><time datetime="{p["date"]}">{heading_time}</time>'
                f'{poster}<div class="post-body">{body_html}</div>{nav}</article>')
        (ROOT / "posts" / f'{p["slug"]}.html').write_text(page(p["title"], body, "../"))

    # archive par année
    by_year = {}
    for p in posts:
        by_year.setdefault(p["date"][:4], []).append(p)
    parts = ['<section><h1>Actualités</h1><p>Concerts, bals, stages et week-ends : toutes les annonces de l\'association, des plus récentes aux plus anciennes.</p></section>']
    for y, ps in by_year.items():
        parts.append(f'<section><h2>{y}</h2><div class="news-grid">' + "".join(card(p, "") for p in ps) + "</div></section>")
    (ROOT / "actualites.html").write_text(page("Actualités", "\n".join(parts), "", "Toutes les actualités de l'association", "archive"))

    # bloc de l'accueil
    block = ('<div class="news-grid">' + "".join(card(p, "") for p in posts[:HOME_COUNT]) + "</div>\n"
             '      <p><a class="button" href="actualites.html">Toutes les actualités et anciens événements</a></p>')
    idx = ROOT / "index.html"
    s = idx.read_text()
    s = re.sub(r"(<!-- NEWS:start -->).*?(<!-- NEWS:end -->)", lambda m: f"{m.group(1)}\n      {block}\n      {m.group(2)}", s, flags=re.S)
    idx.write_text(s)
    print(f"{len(posts)} articles générés")


if __name__ == "__main__":
    main()
