# UK National Offset Council website

The website at https://nationaloffsetcouncil.uk, served by GitHub Pages.

The pages are generated: edit `tools/build_noc.py`, never the HTML, then run `python tools/build_noc.py` from this folder.

Official updates: the GitHub Action "Official updates from GOV.UK" (`.github/workflows/gov-updates.yml`) runs every three hours. It reads GOV.UK's public search with `tools/gov_updates.py`, keeps publications about UK Offset in `data/gov_updates.json`, rebuilds the pages and publishes them. GOV.UK content is re-used under the Open Government Licence v3.0.
