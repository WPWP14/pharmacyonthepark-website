# Pharmacy on the Park website

Source for pharmacyonthepark.com. Every push to `main` rebuilds the site and publishes it with GitHub Pages (see `.github/workflows/deploy.yml`).

- Edit content in `src/` (see `CLAUDE.md` for how everything fits together).
- Build locally: `pip install pillow playwright && python -m playwright install chromium && python build.py`, then open `_site/index.html`.
