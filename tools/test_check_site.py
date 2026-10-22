#!/usr/bin/env python3
"""Tests de tools/check_site.py : on abîme une copie du site et on vérifie que le contrôle le voit.

Usage : python3 tools/test_check_site.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REAL = Path(__file__).resolve().parent.parent


def copie(tmp):
    """Copie du site : pages et outils copiés (modifiables), le reste (images, polices, scripts) en liens."""
    for item in REAL.iterdir():
        if item.name in (".git", "__pycache__"):
            continue
        dest = tmp / item.name
        if item.name in ("posts", "histoire", "tools") or item.is_dir() and (item / "index.html").exists():
            shutil.copytree(item, dest, ignore=shutil.ignore_patterns("__pycache__"))
        elif item.suffix in (".html", ".xml", ".txt"):
            shutil.copy(item, dest)
        else:
            dest.symlink_to(item)


class TestCheckSite(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        copie(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def check(self, *args):
        r = subprocess.run([sys.executable, str(self.tmp / "tools" / "check_site.py"), *args], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_site_actuel_ok(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_page_supprimee(self):
        victime = sorted((self.tmp / "posts").glob("2022-11-06-jam*.html"))[0]
        victime.unlink()
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("page supprimée", out)
        self.assertIn(victime.name, out)

    def test_retrait_voulu(self):
        victime = sorted((self.tmp / "posts").glob("2022-11-06-jam*.html"))[0]
        victime.unlink()
        self.check("--retirer", f"posts/{victime.name}")
        # le lien précédent/suivant des voisines et le plan du site pointent encore vers elle : le contrôle le signale aussi
        code, out = self.check()
        self.assertNotIn("page supprimée", out)

    def test_texte_efface(self):
        page = self.tmp / "posts" / "2026-12-20-jam-forro-de-noel.html"
        page.write_text(page.read_text()[:600] + "</article></main></body></html>")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("beaucoup plus courte", out)

    def test_texte_ecrit_a_la_main_perdu(self):
        page = self.tmp / "posts" / "2026-12-20-jam-forro-de-noel.html"
        texts = json.loads((self.tmp / "tools" / "event_texts.json").read_text())
        frag = texts["2026-12-20-jam-forro-de-noel"][:120]
        page.write_text(page.read_text().replace(frag, "texte importé de Facebook"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("texte rédigé à la main absent", out)

    def test_lien_casse(self):
        page = self.tmp / "actualites.html"
        page.write_text(page.read_text().replace('href="posts/', 'href="postes/', 1))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("lien cassé", out)

    def test_video_absente(self):
        page = self.tmp / "videos.html"
        vid = re.search(r'data-id="([^"]+)"', page.read_text()).group(1)
        page.write_text(page.read_text().replace(f'data-id="{vid}"', 'data-id="x"'))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("vidéo absente", out)

    def test_adresse_du_plan_du_site_introuvable(self):
        sm = self.tmp / "sitemap.xml"
        sm.write_text(sm.read_text().replace("</urlset>", "<url><loc>https://lespiedsontdesoreilles.fr/posts/inexistante.html</loc></url></urlset>"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("plan du site", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
