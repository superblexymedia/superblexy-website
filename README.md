# superblexymedia.com

Static website for Superblexy Media, hosted on Cloudflare Pages.

- Edit page content in `build.py`, styles in `static/css/site.css`, behaviour in `static/js/site.js`.
- Run `python3 build.py` to regenerate `dist/`, then commit. Cloudflare publishes `dist/` automatically on every push to `main`.
- Preview locally: `python3 serve.py`, then open http://127.0.0.1:8787

See MIGRATION-NOTES.md for the Framer move, DNS records and the cutover checklist.
