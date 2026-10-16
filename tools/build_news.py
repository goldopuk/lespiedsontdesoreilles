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
# date réelle de l'événement des articles WordPress (sinon l'article serait classé à sa date de publication)
# fragment du slug WordPress -> date de l'événement (relevée sur la page Facebook de l'association)
EVENT_DATES = {
    "concert-forro-tati-veras": "2026-11-28", "le-bal-tempete-2027": "2027-04-17",
    "stages-de-forro-roots-avec-simon-bagard": "2026-09-26", "concert-everton-corone-trio": "2026-09-26",
    "fete-de-fin-de-saison-des-podos-2": "2026-07-07", "gros-week-end-forro-avec-cristalino": "2026-06-12",
    "bal-tempete": "2026-05-02", "concert-de-saira-et-stages": "2026-04-11",
    "boum-forro-de-la-nouvelle-annee": "2026-01-10", "bal-jam-forro-de-noel-a-saint-nazaire": "2025-12-21",
    "forro-na-chuva-a-saint-nazaire": "2025-11-08", "forro-do-domingo-a-saint-nazaire": "2025-10-19",
    "bal-concert-jam-avec-duo-caldo-de-cana": "2025-09-21", "20-sept-gros-concert-forro": "2025-09-20",
    "bal-concert-trio-forro-pe-de-serra": "2025-07-15", "bal-concert-forro-ateliers-danse": "2025-07-09",
    "sambada-do-brasil-au-kiosq": "2025-06-27", "les-podos-font-la-fete-de-la-musique": "2025-06-21",
    "fete-de-fin-de-saison-des-podos": "2025-06-17", "gros-week-end-forro-forrofia": "2025-05-16",
    "concert-nandinho-barros": "2025-04-19", "concert-carnavalesque-forro-avec-baile-de-rabeca": "2025-03-15",
    "bel-air-de-forro": "2025-02-01", "boum-forro-avec-dj-caraca": "2025-01-04", "bal-jam-forro-de-noel": "2024-12-15",
    "concert-madame-forro": "2024-11-16", "la-sambada-du-kiosq": "2024-10-18", "gandaia-na-ponte-au-skate-park": "2024-06-28",
    "bal-de-fin-dannee-des-podos": "2024-07-02", "concert-forro-lenilda": "2024-05-31",
    "gros-week-end-forro-avec-trio-d2": "2024-04-06", "roda-do-brasil-forro-samba": "2024-03-15",
    "concert-bresilien-carnavalesque": "2024-03-02", "carnaval-de-rue-bresilien": "2024-03-02",
    "the-forroscopics-de-retour": "2024-01-27", "boum-bresilienne-forro-avec-dj-flow": "2024-01-06",
    "pour-les-enfants": "2024-01-05", "gros-week-end-forro-avec-conterraneos": "2023-09-30",
    "apero-forro-commando": "2023-08-24", "fete-des-podos-bal-forro": "2023-07-06", "le-gros-week-end-forro-2023": "2023-06-23",
}


def event_date(slug):
    from urllib.parse import unquote
    slug = unquote(slug)
    return next((d for frag, d in EVENT_DATES.items() if frag in slug), None)


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
    wp_file = ROOT / "tools" / "wp_posters.json"
    if wp_file.exists() and post["slug"] in json.loads(wp_file.read_text()):
        return json.loads(wp_file.read_text())[post["slug"]]
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
      <a href="{prefix}videos.html">Vidéos</a>
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
  <script defer src="{prefix}js/videos.js"></script>
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
    if kind == "archive" and e.get("month"):
        y, m = e["date"][:7].split("-")
        return f"Événement de {MONTHS[int(m) - 1]} {y}", ""
    if kind == "archive":
        if e.get("end"):
            return f'Du {long_date(e["date"])} au {long_date(e["end"])}', ""
        return long_date(e["date"]).capitalize(), ""
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


def video_thumb(vid):
    """Vignette locale de la vidéo YouTube : aucune requête vers Google avant le clic du visiteur."""
    dest = ROOT / "images" / "videos" / f"{vid}.jpg"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        for name in ("maxresdefault", "hqdefault", "mqdefault"):
            r = subprocess.run(["curl", "-fsSL", "--max-time", "30", "-o", str(dest), f"https://i.ytimg.com/vi/{vid}/{name}.jpg"],
                               capture_output=True)
            if r.returncode == 0:
                break
            dest.unlink(missing_ok=True)
    return dest.name if dest.exists() else None


def attach_videos(posts):
    """Rattache les vidéos YouTube (tools/videos.json) aux pages d'événements : date de l'événement + mot-clé du titre."""
    vf = ROOT / "tools" / "videos.json"
    if not vf.exists():
        return
    for rule in json.loads(vf.read_text()):
        found = [p for p in posts if p["date"][:10] == rule["date"] and rule["kw"] in html.unescape(p["title"]).lower()]
        if len(found) != 1:
            print(f'  ! vidéos non rattachées ({len(found)} pages) : {rule["date"]} {rule["kw"]}')
            continue
        found[0].setdefault("videos", []).extend(rule["videos"])


def render_videos(p, prefix):
    if not p.get("videos"):
        return ""
    items = []
    for vid, label in p["videos"]:
        thumb = video_thumb(vid)
        style = f' style="background-image:url({prefix}images/videos/{thumb})"' if thumb else ""
        items.append(
            f'<figure class="video"><button class="video-lite" type="button" data-id="{vid}" data-title="{html.escape(label)}"{style} '
            f'aria-label="Lire la vidéo : {html.escape(label)}"><span class="play" aria-hidden="true"></span></button>'
            f'<figcaption><a href="https://www.youtube.com/watch?v={vid}">{html.escape(label)}</a></figcaption></figure>')
    return ('<section class="videos"><h2>Vidéos</h2>'
            '<p class="note">Les vidéos sont hébergées par YouTube. Elles ne se chargent, et YouTube n\'est contacté, qu\'au moment où vous cliquez sur lecture.</p>'
            f'<div class="video-list">{"".join(items)}</div></section>')


def build_videos_page(posts):
    """Page regroupant toutes les vidéos, avec recherche et filtre par année."""
    import unicodedata as ud
    items = []
    for p in posts:
        for vid, label in p.get("videos", []):
            items.append((p["date"], vid, label, p))
    items.sort(key=lambda x: (x[0], x[2]), reverse=True)
    years = sorted({d[:4] for d, *_ in items}, reverse=True)

    def norm(t):
        return "".join(c for c in ud.normalize("NFD", t.lower()) if not ud.combining(c))

    cards = []
    for d, vid, label, p in items:
        thumb = video_thumb(vid)
        style = f' style="background-image:url(images/videos/{thumb})"' if thumb else ""
        search = norm(f'{label} {html.unescape(p["title"])} {d[:4]} {p.get("event", {}).get("place", "")}')
        cards.append(
            f'<figure class="video" data-year="{d[:4]}" data-search="{html.escape(search)}">'
            f'<button class="video-lite" type="button" data-id="{vid}" data-title="{html.escape(label)}"{style} '
            f'aria-label="Lire la vidéo : {html.escape(label)}"><span class="play" aria-hidden="true"></span></button>'
            f'<figcaption><strong>{html.escape(label)}</strong><br>'
            f'<a href="posts/{p["slug"]}.html">{html.escape(p["title"])}</a> · <time datetime="{d}">{shown_date(p)}</time></figcaption></figure>')
    chips = '<button type="button" class="chip active" data-year="">Toutes</button>' + "".join(
        f'<button type="button" class="chip" data-year="{y}">{y}</button>' for y in years)
    body = (f'<section><h1>Vidéos</h1><p>Concerts, bals et week-ends de l\'association en vidéo : {len(items)} vidéos. '
            'Elles sont hébergées par YouTube et ne se chargent qu\'au clic. '
            '<a href="https://www.youtube.com/@lespiedsontdesoreilles">Toute la chaîne YouTube</a>.</p>'
            '<div class="video-tools"><label class="sr-only" for="video-search">Rechercher une vidéo</label>'
            '<input id="video-search" type="search" placeholder="Rechercher (artiste, lieu, année…)" autocomplete="off">'
            f'<div class="chips" role="group" aria-label="Filtrer par année">{chips}</div>'
            '<p id="video-count" class="note" aria-live="polite"></p></div>'
            f'<div class="video-list video-gallery">{"".join(cards)}</div>'
            '<p id="video-none" hidden>Aucune vidéo ne correspond à cette recherche.</p></section>')
    (ROOT / "videos.html").write_text(page("Vidéos", body, "", "Toutes les vidéos de l'association Les pieds ont des oreilles", "archive"))
    print(f"{len(items)} vidéos sur videos.html")


def upcoming_events(posts, today=None):
    """Événements à venir (date >= aujourd'hui), du plus proche au plus lointain."""
    today = (today or datetime.date.today()).isoformat()
    ev = [p for p in posts if p["date"][:10] >= today and not p.get("month")
          and (p.get("event") or {}).get("kind") != "series"]
    return sorted(ev, key=lambda p: p["date"])


def next_event_box(posts, prefix=""):
    """Carte « prochains rendez-vous » : la liste complète est dans la page, un petit script garde les événements non passés."""
    up = upcoming_events(posts)[:8]
    data = [{"t": html.unescape(p["title"]), "d": p["date"][:10], "l": long_date(p["date"][:10]), "u": f'{prefix}posts/{p["slug"]}.html'} for p in up]
    first = up[0] if up else None
    fallback = (f'<a href="{prefix}posts/{first["slug"]}.html"><strong>{html.escape(first["title"])}</strong></a>'
                f'<span>{long_date(first["date"][:10])}</span>') if first else ""
    return (f'<div class="next-event" data-events=\'{html.escape(json.dumps(data, ensure_ascii=False), quote=True)}\' {"" if first else "hidden"}>'
            f'<span class="next-label">Prochain rendez-vous</span><div class="next-list">{fallback}</div></div>')


def build_hero_preview(posts):
    """Page d'aperçu (non liée, non indexée) : trois propositions d'en-tête sobres pour l'accueil."""
    nxt = next_event_box(posts)
    inscr = "https://www.helloasso.com/beta/associations/les-pieds-ont-des-oreilles/adhesions/inscriptions-podo-2026-27-2"
    heroes = f'''
<p class="preview-label">Proposition 1 · Nuit et photo</p>
<section class="hn" style="background-image:url(images/videos/e9JbtfMRlTI.jpg)">
  <div class="hn-inner">
    <p class="kicker">Association · Saint-Nazaire</p>
    <h1>Musique et danse forró<br>pour tou·te·s</h1>
    <p class="lead">Cours de danse, bals, stages, concerts et ateliers de percussions du Nordeste brésilien.</p>
    <p class="actions"><a class="btn solid" href="{inscr}">S'inscrire pour 2026-27</a><a class="btn line" href="actualites.html">Actualités</a></p>
    {nxt}
  </div>
</section>

<p class="preview-label">Proposition 2 · Papier</p>
<section class="hp">
  <div class="hp-inner">
    <div class="hp-text">
      <p class="kicker">Les pieds ont des oreilles · Saint-Nazaire</p>
      <h1>Musique et danse forró<br>pour tou·te·s</h1>
      <span class="rule" aria-hidden="true"></span>
      <p class="lead">Cours de danse, bals, stages, concerts et ateliers de percussions du Nordeste brésilien.</p>
      <p class="actions"><a class="btn solid dark" href="{inscr}">S'inscrire pour 2026-27</a><a class="btn line dark" href="actualites.html">Actualités</a></p>
    </div>
    <div class="hp-side">
      <img src="images/logo-podo.jpg" alt="Logo Les pieds ont des oreilles" width="422" height="462">
      {nxt}
    </div>
  </div>
</section>

<p class="preview-label">Proposition 3 · Mer et phare</p>
<section class="hm">
  <svg class="hm-art" viewBox="0 0 1200 420" preserveAspectRatio="xMaxYMax meet" aria-hidden="true">
    <g fill="none" stroke="#fdc16d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".9">
      <path d="M990 60 l16 -34 l16 34 z"/><rect x="996" y="60" width="20" height="20"/><path d="M984 80 h44"/>
      <path d="M990 80 l-10 280 h54 l-10 -280"/><path d="M984 150 h44 M981 230 h50 M978 300 h56"/>
      <path d="M1006 40 l-120 -22 M1006 40 l140 -16" opacity=".5"/>
    </g>
    <g fill="none" stroke="#f4813f" stroke-width="1.6" opacity=".75">
      <path d="M0 352 q75 -26 150 0 t150 0 t150 0 t150 0 t150 0 t150 0 t150 0 t150 0"/>
      <path d="M0 376 q75 -26 150 0 t150 0 t150 0 t150 0 t150 0 t150 0 t150 0 t150 0" opacity=".7"/>
      <path d="M0 400 q75 -26 150 0 t150 0 t150 0 t150 0 t150 0 t150 0 t150 0 t150 0" opacity=".5"/>
    </g>
  </svg>
  <div class="hm-inner">
    <p class="kicker">Association · Saint-Nazaire</p>
    <h1>Musique et danse forró<br>pour tou·te·s</h1>
    <p class="lead">Cours de danse, bals, stages, concerts et ateliers de percussions du Nordeste brésilien.</p>
    <p class="actions"><a class="btn solid" href="{inscr}">S'inscrire pour 2026-27</a><a class="btn line" href="actualites.html">Actualités</a></p>
    {nxt}
  </div>
</section>'''
    page_html = page("Aperçu des en-têtes", heroes, "", "", "hero-preview")
    page_html = page_html.replace("<head>", '<head>\n  <meta name="robots" content="noindex">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap">', 1)
    page_html = page_html.replace("</body>", '<script defer src="js/next-event.js"></script>\n</body>', 1)
    (ROOT / "apercu-entete.html").write_text(page_html)


def card(p, prefix):
    if p["poster"]:
        src = f'{prefix}images/affiches/{p["poster"]}'
        # seules les images au format exact des bannières Facebook (16:9) remplissent le cadre ; les autres s'affichent en entier sur fond flouté, sans rognage
        fit = abs(poster_ratio(p["poster"]) - 16 / 9) > 0.04
        thumb = (f'<div class="thumb{" fit" if fit else ""}" style="--bg:url(\'{src}\')">'
                 f'<img src="{src}" alt="Affiche : {html.escape(p["title"])}" loading="lazy"></div>')
    else:
        thumb = '<div class="thumb no-poster" aria-hidden="true"></div>'
    if p.get("videos"):
        thumb = thumb.replace("</div>", '<span class="badge-video">▶ Vidéo</span></div>', 1)
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
        ev_date = event_date(r["slug"])
        posts.append({"title": title, "slug": slug, "date": ev_date or r["date"][:10], "event_dated": bool(ev_date),
                      "raw": r, "poster": poster_of(r)})

    # événements d'archives : fiches Facebook (texte, lieu), séries régulières, affiches seules
    events_file = ROOT / "tools" / "events.json"
    if events_file.exists():
        for e in json.loads(events_file.read_text()):
            posts.append({"title": e["title"], "slug": e["slug"], "date": e["date"], "month": e.get("month", False),
                          "raw": {"content": ""}, "poster": e["poster"], "event": e})
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    attach_videos(posts)
    build_videos_page(posts)
    build_hero_preview(posts)

    for i, p in enumerate(posts):
        if p.get("event"):
            heading_time, body_html = render_event(p["event"])
        else:
            body_html = convert_content(p["raw"]["content"], "../")
            heading_time = long_date(p["date"]).capitalize() if p.get("event_dated") else f'Publié le {shown_date(p)}'
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
                f'{poster}<div class="post-body">{body_html}</div>{render_videos(p, "../")}{nav}</article>')
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
