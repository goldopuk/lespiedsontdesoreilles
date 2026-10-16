#!/bin/bash
# Bascule finale : à lancer APRÈS avoir changé les DNS dans Cloudflare (voir README.md).
# Vérifie les DNS, déclare le domaine à GitHub Pages, attend le certificat HTTPS puis impose HTTPS.
set -euo pipefail
cd "$(dirname "$0")/.."
DOMAIN=lespiedsontdesoreilles.fr
REPO=goldopuk/lespiedsontdesoreilles

echo "1/4 Vérification des DNS…"
IPS=$(dig +short A "$DOMAIN" | sort | tr '\n' ' ')
echo "    $DOMAIN -> $IPS"
if ! echo "$IPS" | grep -q "185.199.10[89].153\|185.199.11[01].153"; then
  echo "ERREUR : le domaine ne pointe pas encore vers GitHub Pages. Attendez la propagation DNS (quelques minutes) et relancez."
  exit 1
fi

echo "2/4 Ajout du fichier CNAME et envoi sur GitHub…"
echo "$DOMAIN" > CNAME
git add CNAME
git commit -m "Domaine personnalisé $DOMAIN" || true
git push

echo "3/4 Déclaration du domaine à GitHub Pages…"
gh api -X PUT "repos/$REPO/pages" -f cname="$DOMAIN" >/dev/null

echo "4/4 Attente du certificat HTTPS (peut prendre jusqu'à ~30 min)…"
for i in $(seq 1 60); do
  STATE=$(gh api "repos/$REPO/pages" --jq '.https_certificate.state // "aucun"')
  echo "    certificat : $STATE"
  if [ "$STATE" = "approved" ]; then
    gh api -X PUT "repos/$REPO/pages" -F https_enforced=true >/dev/null
    echo "OK : https://$DOMAIN est en ligne avec HTTPS imposé."
    exit 0
  fi
  sleep 30
done
echo "Le certificat n'est pas encore prêt : relancez ce script dans un moment (il reprend là où il en était)."
exit 2
