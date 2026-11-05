# Superblexy Media website: Framer → Cloudflare Pages

## What's in this folder

- `backup/`: full copy of the Framer site taken 5 Nov 2026 (6 pages, all images, video, fonts).
- `site/build.py`: all page content lives here. Edit, then run `python3 build.py` to regenerate `site/dist/`.
- `site/static/`: styles (`css/site.css`) and behaviour (`js/site.js`).
- `site/dist/`: the finished website. This folder is what gets published.

## Page addresses (unchanged from Framer)

/  ·  /about  ·  /projects  ·  /services  ·  /contact  ·  /agencies

Extra redirects: /home → /, /portfolio and /work → /projects, /agency → /agencies, /book → Calendly 30-min.

## Contact form

Web3Forms, free plan (250 messages/month). Account: info@superblexymedia.com.
Messages arrive from notify@web3forms.com, currently under Gmail's **Updates** tab.

## DNS snapshot before the move (Namecheap BasicDNS, 5 Nov 2026)

| Record | Value | Action at cutover |
|---|---|---|
| NS | dns1/dns2.registrar-servers.com | Keep: we are NOT moving nameservers |
| @ A | 162.255.119.96 (Namecheap URL redirect → www) | Keep, and confirm it's a permanent (301) redirect |
| www CNAME | sites.framer.app | **Change to the Cloudflare Pages address** |
| @ MX | 1 smtp.google.com | Keep. Google Workspace email |
| @ TXT | google-site-verification=… | Keep |
| SPF | added 5 Nov 2026 | `v=spf1 include:_spf.google.com ~all` |
| DKIM | added 5 Nov 2026 | `google._domainkey` TXT (2048-bit), authentication ON in Google Admin |
| DMARC | added 5 Nov 2026 | `_dmarc` TXT `v=DMARC1; p=none; rua=mailto:info@superblexymedia.com` |
| a A ×2 | 31.43.160.6 / 31.43.161.6 (Framer IPs on host `a`, a typo) | Delete at cutover |

Only the `www` record changes for the website, so email is never touched by the move.

## Hosting

Cloudflare Pages project `superblexy-website` (account info@superblexymedia.com), connected to GitHub `superblexymedia/superblexy-website`, branch `main`, output folder `dist`, no build command. Every push to `main` deploys automatically. Preview: https://superblexy-website.pages.dev

## Cutover checklist

1. New site live on its Cloudflare preview address; every page, video, form and link checked.
2. Add www.superblexymedia.com as a custom domain in Cloudflare Pages.
3. Namecheap → Advanced DNS → change `www` CNAME to the Cloudflare Pages address.
4. Wait for HTTPS to go green; re-check all 6 pages + redirects on the real domain.
5. Google Search Console: submit sitemap.xml and request indexing for the 6 pages.
6. Send a test contact-form message from the live site.
7. Only then: remove the domain from Framer and let the subscription lapse.
