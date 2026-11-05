#!/usr/bin/env python3
"""Builds the Superblexy Media static site into dist/.
Edit the page content below, then run:  python3 build.py
"""
import json, os, shutil, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://www.superblexymedia.com'
CALENDLY = 'https://calendly.com/superblexymedia'
CALENDLY_30 = 'https://calendly.com/superblexymedia/30min'
# Web3Forms access key — free, created at https://web3forms.com with info@superblexymedia.com
WEB3FORMS_KEY = os.environ.get('WEB3FORMS_KEY', '949907a6-a390-45f8-8386-d16c4a79e888')
VERSION = datetime.date.today().strftime('%Y%m%d')

SOCIALS = [
    ('Instagram', 'https://www.instagram.com/superblexy/'),
    ('Tiktok', 'https://www.tiktok.com/@superblexymedia'),
    ('Linkedin', 'https://www.linkedin.com/in/superblexy/'),
]

def esc(s): return html.escape(s, quote=True)

# ---------- components ----------
def yt(vid, label, short=False, eager=False):
    q = 'hqdefault' if short else 'maxresdefault'
    return (f'<button type="button" class="yt{" short" if short else ""}" data-id="{vid}" aria-label="Play video: {esc(label)}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/{q}.jpg" alt="" width="1280" height="720" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async"><span class="play" aria-hidden="true"></span></button>')

def cap(caption):
    if ' | ' in caption:
        kind, who = caption.split(' | ', 1)
        return f'<p class="caption"><span class="kind">{esc(kind)}</span><span class="who">{esc(who)}</span></p>'
    return f'<p class="caption">{esc(caption)}</p>'

def video_item(vid, caption):
    return f'<div class="item">{yt(vid, caption)}{cap(caption)}</div>'

def short_item(vid, caption):
    return f'<div class="item">{yt(vid, caption, short=True)}{cap(caption)}</div>'

LOGOS = [('client-pulse-sports', 'Pulse Sports', 200, 113), ('client-marketing32', 'Marketing32', 160, 161),
         ('client-flinx-realty', 'FlinX Realty', 200, 101), ('client-big-technology-podcast', 'Big Technology Podcast', 160, 155),
         ('client-battabox', 'BattaBox', 160, 143)]

def trusted():
    def row(hidden):
        imgs = ''.join(f'<img src="/img/{f}.webp" alt="{"" if hidden else esc(a)}" width="{w}" height="{h}" loading="lazy">' for f, a, w, h in LOGOS)
        return f'<div class="marquee-set" style="display:flex;gap:inherit;align-items:center"{" aria-hidden=\"true\"" if hidden else ""}>{imgs}</div>'
    sets = row(False) + row(True) + row(True) + row(True)
    return (f'<section class="trusted wrap" aria-labelledby="trusted-h"><h2 id="trusted-h" class="section-title">Trusted by</h2>'
            f'<div class="marquee"><div class="marquee-track">{sets}</div></div></section>')

TESTIMONIALS = [
    ('“A Creative Partner, Not Just an Editor - Lisa”',
     ['Lisa, Director of Marketing at Indiewalls, shares how Superblexy Media transformed their post-production experience.',
      'From struggling to find someone who could run with an idea independently, to having a partner who over-delivers with creative freedom.'],
     'tEemY18SKDo', 'Indiewalls testimonial'),
    ('“The Videos Made People See Us as The Leader in The Industry - Bright”',
     ['FlinX Realty generated over ₦20 million in sales through strategic, appealing videos that connect with the audience.'],
     '0_XKl3nhOWo', 'FlinX Realty testimonial'),
    ('"The Editor Who Gets the Vibe Every Time - Brett"',
     ['Brett Allen, CEO of Marketing32, breaks down why Superblexy Media has become a core part of his team. Speed, communication, creative instinct —',
      "Brett's team shoots regular social media content, and Blessing consistently makes it feel modern, professional, and on-brand without needing a lengthy back-and-forth."],
     '5qAWIfDpCjc', 'Marketing32 testimonial'),
]

def testimonials(boxed=False):
    cards = ''
    for q, paras, vid, label in TESTIMONIALS:
        ps = ''.join(f'<p class="body">{esc(p)}</p>' for p in paras)
        cards += f'<article class="tm"><div class="tm-text"><h3>{esc(q)}</h3>{ps}</div>{yt(vid, label)}</article>'
    inner = (f'<div class="tm-head"><div><p class="section-title">Testimonials</p><h2>Hear it from Our Clients</h2></div>'
             f'<div class="tm-arrows"><button type="button" data-prev aria-label="Previous testimonial">←</button>'
             f'<button type="button" data-next aria-label="Next testimonial">→</button></div></div>'
             f'<div class="tm-track">{cards}</div>')
    if boxed:
        return f'<section class="wrap section" data-carousel><div class="soft tm-boxed">{inner}</div></section>'
    return f'<section class="soft section wrap" data-carousel>{inner}</section>'

def header(active):
    links = [('/', 'Home'), ('/about', 'About'), ('/projects', 'Projects'), ('/services', 'Services'), ('/contact', 'Contact')]
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in links)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="bar wrap">
<a class="brand" href="/"><img src="/img/logo.webp" alt="" width="20" height="21">Superblexy Media</a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div class="header-right"><a class="header-cta" href="{CALENDLY}" target="_blank" rel="noopener">Book a call</a>
<button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></header>'''

def footer():
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in SOCIALS)
    year = datetime.date.today().year
    return f'''<footer class="site-footer"><div class="wrap">
<div class="footer-top"><p>Ready to work magic?</p>
<a class="contact-link" href="/contact">Contact Us<span class="circle" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 12h16M14 6l6 6-6 6"/></svg></span></a></div>
<nav class="socials" aria-label="Social">{soc}<a href="mailto:info@superblexymedia.com">Email</a></nav>
<nav class="footer-pages" aria-label="Footer"><a href="/">Home</a><a href="/about">About</a><a href="/projects">Projects</a><a href="/services">Services</a><a href="/contact">Contact</a></nav>
<div class="footer-legal"><p>Superblexy Media LLC. 815 Brazos St., Ste 500, 78701 Austin TX</p><p>Copyright © {year} Superblexy Media LLC. | All Rights Reserved</p></div>
</div></footer>'''

ORG = {
    "@type": "Organization", "@id": SITE + "/#org", "name": "Superblexy Media", "legalName": "Superblexy Media LLC",
    "url": SITE + "/", "logo": SITE + "/apple-touch-icon.png", "email": "info@superblexymedia.com",
    "description": "Video and podcast editing studio editing podcasts, YouTube and brand content for companies in the US and worldwide.",
    "founder": {"@type": "Person", "name": "Blessing Jimoh", "jobTitle": "Founder"},
    "address": {"@type": "PostalAddress", "streetAddress": "815 Brazos St., Ste 500", "addressLocality": "Austin",
                "addressRegion": "TX", "postalCode": "78701", "addressCountry": "US"},
    "sameAs": [u for _, u in SOCIALS],
}

def page(path, title, desc, og, body, active=None, schema=None, preload=''):
    url = SITE + ('/' if path == '/' else path)
    graph = [ORG, {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Superblexy Media", "publisher": {"@id": SITE + "/#org"}},
             {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#site"}}]
    if schema: graph += schema
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Superblexy Media">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/img/{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/img/{og}.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#000000">
<link rel="preload" href="/fonts/outfit-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/outfit-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="preconnect" href="https://i.ytimg.com">
<link rel="stylesheet" href="/css/site.css?v={VERSION}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/js/site.js?v={VERSION}" defer></script>
</body>
</html>
'''

# ---------- pages ----------
SERVICES = [
    ('Podcast & Video Editing', 'Our core service. We edit video podcasts, YouTube episodes and short-form clips for teams in the US and worldwide, story-first and delivered in 48 hours. We also shoot culture videos, testimonials and documentaries with real people.'),
    ('Photography', 'Video and photography often go hand in hand. We capture genuine moments with real people, plus corporate headshots and photos tailored for your website and social media.'),
    ('Animated Videos', 'Turn complex ideas into captivating visuals that are easy to understand. Animation lifts viewer engagement and breaks down the complexity of your product or service.'),
    ('Content Development', "Great videos start with great content: the right script. We help shape your brand’s story, voice and vision before anything is filmed or edited."),
    ('Audio Production', 'Audio production for podcasts, music and voiceovers. We record, mix and master to industry standards, with careful sound editing, noise reduction and level balancing.'),
]

def home():
    works = [('oEVHNvE_jDw', 'Video Podcast | Big Technology Podcast ft. Mark Cuban'), ('pjMGwskfcms', 'Menswear YouTube | Sebastian De Castro'),
             ('aQc1zsFHP30', 'Documentary YouTube | The Black Wealth Explainer'), ('rkwn3Xlcij0', 'Project Recap Video | Indiewalls'),
             ('vxBmZoZeelw', 'Education YouTube Content | The Family Trader'), ('_SqrzPiNTPg', 'Video Ads | Flinx Realty')]
    items = ''.join(f'<div class="ruled-item"><h3>{t}</h3><p class="body">{esc(d)}</p></div>' for t, d in SERVICES)
    body = f'''<section class="hero-split wrap">
<h1 class="display">We Edit Video &amp; Podcast<br class="br-lg"> Stories That Convert</h1>
<div><p class="lead">We're a team of editors crafting podcasts, YouTube and brand content for companies in the US and worldwide. Story-first edits, delivered in 48 hours.</p>
<div class="hero-actions"><a class="btn btn-black" href="{CALENDLY_30}" target="_blank" rel="noopener">Book a call</a><a class="btn btn-outline" href="/projects">See our work</a></div></div>
</section>
<video class="hero-video" src="/media/hero.mp4" poster="/media/hero-poster.webp" autoplay muted loop playsinline preload="metadata" aria-label="Superblexy Media showreel"></video>
<section class="dark section wrap" aria-labelledby="works-h">
<h2 id="works-h" class="section-title" style="margin-bottom:40px">Featured Works</h2>
<div class="vgrid">{''.join(video_item(v, c) for v, c in works)}</div>
</section>
{trusted()}
<section class="wrap section ruled" aria-labelledby="svc-h" style="padding-top:24px">
<h2 id="svc-h" class="section-title">Services</h2>
<div class="ruled-grid">{items}<img class="ruled-photo" src="/img/beach-shoot.webp" alt="Superblexy Media crew filming a two-person scene on a Lagos beach" width="1100" height="1375" loading="lazy"></div>
</section>
{testimonials()}'''
    return page('/', 'Superblexy Media | Video & Podcast Editing Studio',
                'Superblexy Media is a video and podcast editing studio. Our team edits podcasts, YouTube and brand content for companies in the US and worldwide, with story-first edits delivered in 48 hours.',
                'og-home', body, '/', preload='<link rel="preload" href="/media/hero-poster.webp" as="image">\n')

def about():
    imgs = [('bts-1', 'Blessing Jimoh editing audio in the studio'), ('bts-2', 'Blessing on set at an indoor sports arena'),
            ('bts-3', 'Blessing with a gimbal camera rig'), ('bts-4', 'Superblexy crew on a podcast set'),
            ('bts-5', 'Podcast guest on a Superblexy shoot'), ('bts-6', 'Behind the scenes on a Superblexy production'),
            ('bts-7', 'Behind the scenes on a Superblexy production'), ('bts-8', 'Behind the scenes on a Superblexy shoot'),
            ('bts-9', 'Behind the scenes on a Superblexy shoot')]
    def im(i, w, h): f, a = imgs[i]; return f'<img src="/img/{f}.webp" alt="{a}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    gallery = (f'<div class="row r3">{im(0,854,999)}{im(1,855,999)}{im(2,855,999)}</div>'
               f'<div class="row r2">{im(3,1234,1361)}{im(4,1150,1361)}</div>'
               f'<div class="row r2b">{im(5,854,999)}{im(6,855,999)}</div>'
               f'<div class="row r2">{im(7,1300,1733)}{im(8,1300,1733)}</div>')
    body = f'''<section class="about-hero wrap">
<p class="section-title">Who is Superblexy Media</p>
<h1 class="display">Fueled by Passion,<br class="br-lg"> Framed by Vision</h1>
<div class="about-stage">
<img class="side-photo" src="/img/about-studio.webp" alt="Superblexy Media filming a seated interview in a studio" width="600" height="631" loading="lazy">
<img class="portrait" src="/img/blessing-jimoh.webp" alt="Blessing Jimoh, founder of Superblexy Media" width="1100" height="1467" fetchpriority="high">
<p class="intro">I'm Blessing Jimoh, founder of Superblexy Media. I grew up around my father's cameras, started editing at 8, and was getting paid for it by 12. Superblexy Media is what that obsession grew into.</p>
</div></section>
<section class="about-story wrap">
<h2>From One Editor to a Full Team</h2>
<div class="copy"><p>What started as one kid at a computer is now a Lagos-based team of video editors, a videographer, a graphic designer and a social media manager, editing for clients across the US and worldwide.</p>
<p>Together, we’ve edited for clients whose combined audiences reach over 200 million monthly viewers, from the Big Technology Podcast to Indiewalls. Every project still runs on what I started with: story first, everything else after.</p></div>
</section>
<section class="dark section wrap" aria-labelledby="bts-h">
<h2 id="bts-h" class="section-title" style="margin-bottom:32px">Behind The lens</h2>
<div class="gallery">{gallery}</div>
</section>'''
    return page('/about', 'About Superblexy Media | Founded by Blessing Jimoh',
                'Founded by Blessing Jimoh, Superblexy Media is a Lagos-based team of editors and creatives editing podcasts, YouTube and brand content for clients in the US and worldwide.',
                'og-about', body, '/about',
                schema=[{"@type": "AboutPage", "url": SITE + "/about", "mainEntity": {"@id": SITE + "/#org"}}])

def projects():
    works = [('rkwn3Xlcij0', 'Project Recap Video | Indiewalls'), ('vxBmZoZeelw', 'Education YouTube Content | The Family Trader'),
             ('jJpBoa06We0', 'Podcast | Big Technology Podcast'), ('_SqrzPiNTPg', 'Video Ads | Flinx Realty'),
             ('iZPzWjfAt_o', 'Interview | Mikel Obi, Pulse Sports'), ('quIYYERMqYk', 'Event Recap | Awoof Sports')]
    shorts = [('YK3xsbIbk7Q', 'Podcast Shorts | Big Tech'), ('XOvZu31v9Hg', 'Sports Updates | Pulse Sports'),
              ('FeSWz2_DXUA', 'Talking Head Shorts | Sebastian'), ('-COYBrNiFFY', 'Superblexy Media | Reel')]
    body = f'''<section class="wrap" style="padding-top:56px;padding-bottom:28px">
<h1 class="display" style="max-width:820px">Our Work: Podcast, YouTube &amp; Brand Videos</h1>
<p class="lead" style="margin-top:14px;max-width:620px">Take a sneak peek at some of the stories we’ve edited 😮‍💨</p></section>
<section class="wrap" style="padding-bottom:64px" aria-label="Long-form projects">
<div class="vgrid" style="gap:40px 20px">{''.join(video_item(v, c) for v, c in works)}</div></section>
<section class="wrap section" aria-labelledby="reels-h" style="padding-top:8px">
<h2 id="reels-h" class="section-title" style="text-align:center;margin-bottom:28px">Reels &amp; Quick Takes</h2>
<div class="shorts">{''.join(short_item(v, c) for v, c in shorts)}</div></section>
{testimonials()}'''
    return page('/projects', 'Our Work: Podcast, YouTube & Brand Videos | Superblexy Media',
                'See podcast, YouTube, documentary and brand videos edited by Superblexy Media for the Big Technology Podcast, Indiewalls, FlinX Realty, Pulse Sports and more.',
                'og-projects', body, '/projects')

def services():
    cards = ''.join(f'<article class="card"><p class="num">{i+1:02d}</p><h3>{t}</h3><p class="body">{esc(d)}</p></article>' for i, (t, d) in enumerate(SERVICES))
    steps = [('Send your footage', 'Share raw files and your style guide.'), ('We edit', 'First cut in 48 hours, built around the story.'),
             ('Revise & deliver', 'Notes, polish, and files ready to publish.')]
    st = ''.join(f'<div class="step"><p class="num">{i+1:02d}</p><h3>{esc(t)}</h3><p class="body">{esc(d)}</p></div>' for i, (t, d) in enumerate(steps))
    shorts = [('l0ASc0oUpWc', 'Interview | Mikel Obi, Pulse Sports'), ('XOvZu31v9Hg', 'Sports Updates | Pulse Sports'),
              ('HYNNJ2YejAw', 'Face Off Fight Night 3 | Pulse Sports'), ('5ia3C4sHBRg', 'Superblexy Media | Reel')]
    body = f'''<section class="dark"><div class="hero-dark wrap">
<div><p class="eyebrow">What we do</p>
<h1 class="display">Story-First Editing for Podcasts, Creators &amp; Brands.</h1>
<p class="lead">A Lagos-based team editing for clients across the US and worldwide. First cut in 48 hours.</p>
<div class="hero-actions"><a class="btn btn-solid" href="{CALENDLY_30}" target="_blank" rel="noopener">Book a Call</a><a class="btn btn-ghost" href="/projects">See Our Work</a></div></div>
<div class="hero-media">{yt('pjMGwskfcms', 'Sebastian De Castro, YouTube', eager=True)}<p class="caption">Sebastian De Castro, YouTube</p></div>
</div></section>
{trusted()}
<section class="wrap section" style="padding-top:16px" aria-label="Services"><div class="cards">{cards}</div></section>
<section class="wrap section" aria-labelledby="how-h" style="padding-top:24px"><h2 id="how-h" class="narrow-title">How We Work</h2><div class="steps">{st}</div></section>
<section class="wrap section" aria-labelledby="sr-h"><h2 id="sr-h" class="section-title" style="text-align:center;margin-bottom:28px">Shorts &amp; Reels</h2>
<div class="shorts">{''.join(short_item(v, c) for v, c in shorts)}</div></section>
<section class="dark"><div class="cta-band wrap"><h2>Have a project in mind?</h2><a class="btn btn-solid" href="{CALENDLY_30}" target="_blank" rel="noopener">Book a Call</a></div></section>'''
    offer = [{"@type": "Service", "name": t, "description": d, "provider": {"@id": SITE + "/#org"}, "areaServed": "Worldwide"} for t, d in SERVICES]
    return page('/services', 'Services | Podcast & Video Editing | Superblexy Media',
                'Podcast, YouTube and short-form editing, plus photography, animation, scripting and audio. Editing for clients in the US and worldwide. First cut in 48 hours.',
                'og-home', body, '/services', schema=offer)

def contact():
    body = f'''<div class="contact-grid wrap">
<section class="contact-wrap">
<h1>Hey! Let’s Work Together 😉</h1>
<form id="contact-form" class="form" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
<input type="hidden" name="subject" value="New enquiry from superblexymedia.com">
<input type="hidden" name="from_name" value="Superblexy Media website">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="field"><span class="sr-only">Your Name (required)</span><input name="name" type="text" placeholder="Your Name *" autocomplete="name" required></label>
<label class="field"><span class="sr-only">Email (required)</span><input name="email" type="email" placeholder="Email *" autocomplete="email" required></label>
<label class="field"><span class="sr-only">Phone Number</span><input name="phone" type="tel" placeholder="Phone Number" autocomplete="tel"></label>
<label class="field"><span class="sr-only">Website</span><input name="website" type="text" placeholder="Website" autocomplete="url"></label>
<label class="field"><span class="sr-only">Tell us about your project (required)</span><textarea name="message" placeholder="Tell us about your project*" required></textarea></label>
<button class="btn btn-black" type="submit">Submit</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form></section>
<section class="book" aria-labelledby="book-h">
<h2 id="book-h">or Book a Call</h2>
<p class="note"><a href="{CALENDLY_30}" target="_blank" rel="noopener" style="text-decoration:underline;text-underline-offset:3px">Calendar not loading? Book here</a></p>
<div class="calendly-inline-widget" data-url="{CALENDLY_30}?hide_gdpr_banner=1"></div>
</section></div>'''
    return page('/contact', 'Contact Superblexy Media | Work with Us',
                'Tell us about your podcast, YouTube or brand video project, or book a 30-minute call with Superblexy Media.',
                'og-contact', body, '/contact', schema=[{"@type": "ContactPage", "url": SITE + "/contact"}])

def agencies():
    blocks = [
        ('The Offer', 'Your video podcast, edited under your brand: the full episode plus 5 vertical clips, delivered in 3 business days (48-hour priority available at +25%). Start with a paid pilot episode for $295, credited against your first month if you sign within 14 days. Monthly plans: Starter $1,049 for 4 episodes, Growth $1,899 for 8 episodes, Scale $3,499 for 16 episodes.'),
        ('Invisible by Design', 'We work behind your brand. Your clients never see our name, and you keep the margin.'),
        ('Fast, Reliable Turnaround', 'Standard turnaround is 3 business days, with 48-hour priority available for +25%. We regularly deliver the Big Technology Podcast’s episodes and Shorts on tight deadlines, sometimes in under 24 hours.'),
        ('How It Works', "Send raw files and your brand guide. We match your style on episode one, you give notes, and from there it’s plug-and-play. Need more volume? Our team scales with you."),
        ('Who We Edit For', '“Nobody does it better than Superblexy! Great team, quality work, and fun times always.” — Alex Kantrowitz, host of the Big Technology Podcast. We also edit for Sebastian De Castro, The Black Wealth Explainer, Indiewalls and Marketing32.'),
    ]
    items = ''.join(f'<div class="ruled-item{" wide" if i == 0 else ""}"><h3>{t}</h3><p class="body">{esc(d)}</p></div>' for i, (t, d) in enumerate(blocks))
    shorts = [('ifaHUn8BViQ', 'Podcast Short | Big Technology Podcast'), ('NpePJw4rVnQ', 'Podcast Short | Big Technology Podcast'),
              ('qwQYWiIxF9M', 'YouTube Short | Sebastian De Castro'), ('4Yif2azUjH0', 'YouTube Short | Sebastian De Castro')]
    body = f'''<section class="dark"><div class="hero-dark wrap">
<div><p class="eyebrow">For podcast &amp; video agencies</p>
<h1 class="display">Your Podcast Editing Team, Under Your Brand.</h1>
<p class="lead">Full episode + 5 vertical clips, delivered under your brand. 3 business-day turnaround; 48-hour priority available. From the team behind the Big Technology Podcast.</p>
<div class="pills"><span class="pill">Paid pilot $295</span><span class="pill">From $1,049/month · 4 episodes</span></div>
<div class="hero-actions"><a class="btn btn-solid" href="{CALENDLY}" target="_blank" rel="noopener">Book a Call</a></div></div>
<div class="hero-media">{yt('oEVHNvE_jDw', 'Big Technology Podcast ft. Mark Cuban', eager=True)}<p class="caption">Big Technology Podcast ft. Mark Cuban</p></div>
</div></section>
{trusted()}
<section class="wrap section" style="padding-top:16px" aria-label="White-label offer"><div class="ruled-grid">{items}</div></section>
{testimonials(boxed=True)}
<section class="wrap section" aria-labelledby="clips-h"><h2 id="clips-h" class="section-title" style="text-align:center;margin-bottom:28px">Podcast Clips &amp; Shorts</h2>
<div class="shorts">{''.join(short_item(v, c) for v, c in shorts)}</div></section>'''
    svc = [{"@type": "Service", "name": "White-label podcast editing for agencies", "provider": {"@id": SITE + "/#org"},
            "description": "Full podcast episode plus 5 vertical clips, edited under your agency's brand with a 3 business-day turnaround.",
            "offers": [{"@type": "Offer", "name": "Paid pilot episode", "price": "295", "priceCurrency": "USD"},
                       {"@type": "Offer", "name": "Starter: 4 episodes/month", "price": "1049", "priceCurrency": "USD"},
                       {"@type": "Offer", "name": "Growth: 8 episodes/month", "price": "1899", "priceCurrency": "USD"},
                       {"@type": "Offer", "name": "Scale: 16 episodes/month", "price": "3499", "priceCurrency": "USD"}]}]
    return page('/agencies', 'White-Label Podcast Editing for Agencies | Superblexy Media',
                'Full episode + 5 vertical clips, delivered under your brand. 3 business-day turnaround; 48-hour priority available. From the team behind the Big Technology Podcast.',
                'og-home', body, schema=svc)

def notfound():
    body = '''<section class="notfound"><h1 class="display">Page not found</h1>
<p class="lead">The page you're looking for has moved or doesn't exist.</p>
<p><a class="btn btn-black" href="/">Back to home</a></p></section>'''
    return page('/404', 'Page not found | Superblexy Media', 'This page could not be found.', 'og-home', body).replace(
        '<meta name="robots" content="max-image-preview:large">', '<meta name="robots" content="noindex">')

# ---------- write ----------
PAGES = {'index.html': home, 'about.html': about, 'projects.html': projects, 'services.html': services,
         'contact.html': contact, 'agencies.html': agencies, '404.html': notfound}

def main():
    for sub in ('css', 'js'):
        shutil.copytree(os.path.join(ROOT, 'static', sub), os.path.join(DIST, sub), dirs_exist_ok=True)
    for name, fn in PAGES.items():
        with open(os.path.join(DIST, name), 'w', encoding='utf-8') as f: f.write(fn())
    today = datetime.date.today().isoformat()
    urls = ['/', '/about', '/contact', '/projects', '/services', '/agencies']
    sm = ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>' for u in urls)
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    open(os.path.join(DIST, '_headers'), 'w').write('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
/img/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/media/*
  Cache-Control: public, max-age=2592000
/css/*
  Cache-Control: public, max-age=31536000, immutable
/js/*
  Cache-Control: public, max-age=31536000, immutable
''')
    # Old/alternate paths people might have linked → correct pages (301)
    open(os.path.join(DIST, '_redirects'), 'w').write('''/home / 301
/portfolio /projects 301
/work /projects 301
/agency /agencies 301
/book https://calendly.com/superblexymedia/30min 302
''')
    print('built', len(PAGES), 'pages →', DIST)

if __name__ == '__main__':
    main()
