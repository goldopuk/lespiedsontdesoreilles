# Site Les pieds ont des oreilles

Site statique (HTML/CSS), contenu repris de l'ancien site WordPress.com. Hébergé sur GitHub Pages, domaine chez Gandi.

## Contenu
- `index.html` : accueil (toutes les sections), à éditer à la main
- `style.css` : styles (thème clair/sombre automatique)
- `actualites.html`, `posts/` : archive et pages des 43 articles (générés)
- `reglement-interieur/`, `mentions-legales/`, `activites*/` : pages reprises de WordPress (générées)
- `about/`, `contact/`, `2023/…` etc. : redirections des anciennes adresses WordPress (générées)
- `images/` : logo, phare, vagues, `affiches/`
- `tools/` : scripts de génération et export WordPress (`posts.json`, `pages.json`)

Régénérer les pages après modification des scripts ou des exports :

```
python3 tools/build_news.py && python3 tools/build_pages.py
```

Voir le site en local : `python3 -m http.server 8765` puis http://localhost:8765

## Mise en ligne sur lespiedsontdesoreilles.fr

Situation constatée le 16/10/2026 : le domaine est enregistré chez **Gandi**, mais ses serveurs de noms sont ceux de **Cloudflare**
(`mary.ns.cloudflare.com`, `cody.ns.cloudflare.com`). Les enregistrements DNS se modifient donc **dans Cloudflare**, pas chez Gandi.
Le site pointe aujourd'hui vers WordPress.com (`A 192.0.78.24` et `192.0.78.25`).

Le courrier du domaine (`MX` Gandi), le `SPF` et les enregistrements Brevo (newsletter, `brevo-code`, `_dmarc`) **ne doivent pas être touchés**.

### 1. Dans Cloudflare (tableau de bord du domaine > DNS > Enregistrements)
1. Supprimer les 2 enregistrements `A` du domaine (`@`) vers `192.0.78.24` et `192.0.78.25`.
2. Ajouter 4 enregistrements `A` sur `@` (nom : `lespiedsontdesoreilles.fr`), tous en **« DNS uniquement »** (nuage gris, pas orange) :
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. (facultatif) 4 enregistrements `AAAA` sur `@` : `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
4. Remplacer l'enregistrement `www` (aujourd'hui un `CNAME` vers le domaine) par un `CNAME` `www` -> `goldopuk.github.io`, en « DNS uniquement ».
5. Ne rien changer d'autre.

### 2. Bascule côté GitHub
Quand le domaine répond (quelques minutes, `dig +short A lespiedsontdesoreilles.fr` doit montrer des `185.199.x.153`) :
```
tools/go_live.sh
```
Le script vérifie les DNS, ajoute le fichier `CNAME`, déclare le domaine à GitHub Pages, attend le certificat HTTPS
(jusqu'à ~30 min) puis impose HTTPS. Il peut être relancé sans risque.

### 3. Après la bascule
- Vérifier https://lespiedsontdesoreilles.fr, https://www.lespiedsontdesoreilles.fr et une ancienne adresse (par exemple `/2026/04/21/bal-tempete/`).
- Facultatif, plus tard : passer les enregistrements en « Proxifié » (nuage orange) avec le mode SSL « Complet (strict) » dans Cloudflare.
- Ne résilier WordPress.com qu'une fois le nouveau site vérifié.

### Retour en arrière
Remettre les deux `A` `192.0.78.24` et `192.0.78.25` et l'ancien `CNAME` `www` dans Cloudflare : le site WordPress redevient visible en quelques minutes.

## Reste à faire
- formulaire de contact (la newsletter renvoie vers le formulaire Brevo de l'ancien site)
- vérifier les mentions légales (hébergeur remplacé par GitHub)
