git pull --rebase origin main
python bibtex_cleanup.py
git add zotero_clean.bib
git commit -m "auto update zotero_clean.bib"
git push origin main
