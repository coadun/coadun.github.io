#!/usr/bin/env python3
"""Build the Coadun blog pages.

The header and footer are copied from the homepage (index.html), so the blog
always matches the main site. Each post can have a cover photo: put <cover>.webp (cards) and <cover>.jpg
(social share image; LinkedIn doesn't reliably show WebP) in
assets/img/blog/, 16:9, and set "cover" on the post. Run from the repo root after adding or editing a
post:

    python3 _blog/build.py

To add a post: write its body HTML in _blog/posts/<slug>.html, add an entry to
POSTS below, then run the script. It writes blog/index.html and
blog/<slug>/index.html. Folders starting with "_" are not published by GitHub
Pages, so _blog/ stays private to the repo.

In a post body, a line like
    <!--FIGURE:file.png|alt text|caption-->
becomes a figure using assets/img/blog/file.png (skipped if the file is missing).
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://coadun.net"

PODCAST_EP1 = {
    "@type": "VideoObject",
    "name": "The Coadun Podcast Ep 1: Switching Off SAS Without Blowing Up Your Timeline",
    "embedUrl": "https://www.youtube-nocookie.com/embed/D2otx501hc8",
    "thumbnailUrl": "https://i.ytimg.com/vi/D2otx501hc8/hqdefault.jpg",
    "uploadDate": "2026-10-27",
    "description": "Esther Gillespie (Jumping Rivers) and James McDermott (Achieve Intelligence) on moving a regulated organisation off SAS without the project overrunning.",
}

# Newest first is not required; the script sorts by date.
POSTS = [
    {
        "slug": "introducing-r-alongside-sas",
        "title": "Introducing R Alongside SAS: Managing Change and Validation in Pharma",
        "date": "2026-11-18",
        "summary": "Key points from the first episode of The Coadun Podcast: why pharma built its own software, why a fixed SAS switch-off date backfires, and how to avoid over-validating.",
        "video": PODCAST_EP1,
        "cover": "introducing-r-alongside-sas",
        "cover_alt": "The Coadun Podcast: James McDermott and Esther Gillespie in conversation",
    },
    {
        "slug": "why-we-built-coadun",
        "title": "Why Jumping Rivers and Achieve Intelligence built Coadun to modernise statistical computing environments",
        "date": "2026-10-29",
        "summary": "Why harmonising a pharma SCE needs both enterprise architecture and open-source depth, how Coadun's three phases work, and who we work with.",
        "video": PODCAST_EP1,
        "cover": "why-we-built-coadun",
        "cover_alt": "Coadun logo, with Jumping Rivers + Achieve Intelligence",
    },
]

CSS = [
    "bootstrap.min.css", "font-awesome.min.css", "themify-icons.css",
    "flaticon-set.css", "animate.css", "validnavs.css", "helper.css",
    "style.css", "responsive.css", "blog.css",
]


def nice_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def absolutise(s):
    """Make homepage-relative links work from /blog/ subfolders."""
    s = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', s)
    s = s.replace('href="index.html"', 'href="/"')
    s = re.sub(r'(src|href)="assets/', r'\1="/assets/', s)
    return s.replace("url(assets/", "url(/assets/")


def chrome():
    src = open(os.path.join(ROOT, "index.html")).read()
    header = src[src.index("    <header>"):src.index("    </header>") + len("    </header>")]
    footer = src[src.index("    <footer"):src.index("  </body>")]
    return absolutise(header), absolutise(footer)


def page(title, desc, url, body, og_type="website", ld=None, image=None):
    header, footer = chrome()
    css = "".join(f'    <link href="/assets/css/{c}" rel="stylesheet" />\n' for c in CSS)
    ld_tag = (f'    <script type="application/ld+json">{json.dumps(ld)}</script>\n' if ld else "")
    t, d = html.escape(title), html.escape(desc)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{t}</title>
    <meta name="description" content="{d}" />
    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:title" content="{t}" />
    <meta property="og:description" content="{d}" />
    <meta property="og:image" content="{image or SITE + '/assets/img/coadun_banner.png'}" />
    <meta property="og:site_name" content="Coadun" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="shortcut icon" href="/assets/img/favicon.png" type="image/x-icon" />
{css}{ld_tag}  </head>

  <body>
{header}
{body}
{footer}  </body>
</html>
"""


def figures(body):
    def repl(m):
        fname, alt, caption = m.group(1).split("|")
        if not os.path.exists(os.path.join(ROOT, "assets/img/blog", fname)):
            return ""
        return (f'          <figure class="post-figure">\n'
                f'            <img src="/assets/img/blog/{fname}" alt="{html.escape(alt)}" loading="lazy" />\n'
                f'            <figcaption>{html.escape(caption)}</figcaption>\n'
                f'          </figure>')
    return re.sub(r"<!--FIGURE:(.+?)-->", repl, body)


def cover_url(p):
    if p.get("cover"):
        return f"{SITE}/assets/img/blog/{p['cover']}.jpg"
    return f"{SITE}/assets/img/coadun_banner.png"


def build_post(p):
    body = figures(open(os.path.join(ROOT, "_blog/posts", p["slug"] + ".html")).read())
    url = f"{SITE}/blog/{p['slug']}/"
    content = f"""    <div class="blog-banner">
      <div class="container">
        <div class="row"><div class="col-lg-8 offset-lg-2">
          <a class="back-link" href="/blog/"><i class="fas fa-arrow-left me-2"></i>All posts</a>
          <h1>{html.escape(p['title'])}</h1>
          <p class="post-meta"><time datetime="{p['date']}">{nice_date(p['date'])}</time></p>
        </div></div>
      </div>
    </div>

    <div class="default-padding">
      <div class="container">
        <article class="post-body">
{body.rstrip()}
        </article>
        <div class="post-footer">
          <p><strong>Want to talk about your SCE?</strong> Book an introductory session with the team.</p>
          <a href="/#contact" class="btn btn-theme fw-bold coadun-border-radius px-4 py-2">Book an introductory session <i class="fas fa-arrow-right ms-2"></i></a>
        </div>
      </div>
    </div>
"""
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": p["summary"],
        "datePublished": p["date"],
        "url": url,
        "image": cover_url(p),
        "author": {"@type": "Organization", "name": "Coadun", "url": f"{SITE}/"},
        "publisher": {"@type": "Organization", "name": "Coadun", "url": f"{SITE}/"},
    }
    if p.get("video"):
        ld["video"] = p["video"]
    out = os.path.join(ROOT, "blog", p["slug"])
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w") as f:
        f.write(page(f"{p['title']} | Coadun", p["summary"], url, content, "article", ld, cover_url(p)))


def build_index(posts):
    def card(p):
        cover = ""
        if p.get("cover"):
            cover = (f'''
              <div class="post-card-cover">
                <img src="/assets/img/blog/{p['cover']}.webp" alt="{html.escape(p.get('cover_alt', ''))}" loading="lazy" width="1280" height="720" />
              </div>''')
        return f"""          <div class="col-lg-4 col-md-6 mb-4">
            <a class="post-card" href="/blog/{p['slug']}/">{cover}
              <div class="post-card-body">
                <p class="post-meta"><time datetime="{p['date']}">{nice_date(p['date'])}</time></p>
                <h3>{html.escape(p['title'])}</h3>
                <p>{html.escape(p['summary'])}</p>
                <span class="read-more">Read the post <i class="fas fa-arrow-right ms-2"></i></span>
              </div>
            </a>
          </div>"""
    cards = "\n".join(card(p) for p in posts)
    content = f"""    <div class="blog-banner">
      <div class="container">
        <div class="row"><div class="col-lg-8 offset-lg-2 text-center">
          <h1>Blog</h1>
          <p>News and thinking from the Coadun team on modernising Statistical Computing Environments.</p>
        </div></div>
      </div>
    </div>

    <div class="default-padding bg-gray">
      <div class="container">
        <div class="row">
{cards}
        </div>
      </div>
    </div>
"""
    with open(os.path.join(ROOT, "blog", "index.html"), "w") as f:
        f.write(page("Blog | Coadun",
                     "News and thinking from Coadun on SCE transformation in pharma and life sciences.",
                     f"{SITE}/blog/", content))


def build_sitemap(posts):
    path = os.path.join(ROOT, "sitemap.xml")
    s = open(path).read()
    s = re.sub(r"\s*<url>\s*<loc>https://coadun\.net/blog/.*?</url>", "", s, flags=re.S)
    entries = [(f"{SITE}/blog/", max(p["date"] for p in posts), "weekly", "0.7")]
    entries += [(f"{SITE}/blog/{p['slug']}/", p["date"], "yearly", "0.6") for p in posts]
    block = "".join(f"""
  <url>
    <loc>{loc}</loc>
    <lastmod>{mod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
  </url>""" for loc, mod, freq, pri in entries)
    s = s.replace("\n</urlset>", block + "\n</urlset>").replace(" \n" + block.lstrip("\n"), block.lstrip("\n"))
    with open(path, "w") as f:
        f.write(s)


if __name__ == "__main__":
    posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    for p in posts:
        build_post(p)
    build_index(posts)
    build_sitemap(posts)
    print(f"Built {len(posts)} posts")
