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

## Mise en ligne (GitHub Pages + Gandi)
1. Créer un dépôt GitHub, y pousser le dossier (`.nojekyll` est déjà là ; le fichier `CNAME` contenant `lespiedsontdesoreilles.fr` n'est ajouté qu'au moment de la bascule du domaine).
2. Dépôt > Settings > Pages : source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Même page : domaine personnalisé `lespiedsontdesoreilles.fr`, puis cocher « Enforce HTTPS » une fois le certificat prêt.
4. Chez Gandi (Nom de domaine > Enregistrements DNS), remplacer les enregistrements de WordPress.com par :
   - 4 enregistrements `A` sur `@` : `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - 1 `CNAME` sur `www` : `<compte-github>.github.io.`
   (vérifier ces adresses sur la doc GitHub Pages avant de les saisir)
5. Ne résilier WordPress.com qu'une fois le nouveau site visible sur le domaine.

## Reste à faire
- formulaire de contact (la newsletter renvoie vers le formulaire Brevo de l'ancien site)
- vérifier les mentions légales (hébergeur remplacé par GitHub)
