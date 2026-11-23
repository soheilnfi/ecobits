# EcoBits static site

Static HTML preview of the EcoBits site. Every page is a single self-contained HTML file (CSS, scripts and the font are inlined). Live preview: https://soheilnfi.github.io/ecobits/

## Run locally

```bash
python3 -m http.server 8417
```

Then open http://localhost:8417/index.html

## Files

| Path | What it is |
|---|---|
| `index.html` | Home page (hero only, one screen, five trade-box looks to compare via `?box=1`…`?box=5`) |
| `landing.html` | Same page as `index.html` without the outer `<!doctype>` wrapper line; other pages link here |
| `coin-*.html`, `coin.html` | One page per asset (`coin.html` is a copy of `coin-btc.html`) |
| `about.html`, `faq.html`, `contact.html`, `terms.html`, `status.html` | Content pages |
| `blog*.html` | Blog archive, posts, category and tag pages, all generated |
| `tools/build-blog.py` | Builds the blog pages from the post list inside it; run `python3 tools/build-blog.py` |
| `assets/coins/` | Coin renders (WebP, from the purchased 3D coin pack) |
| `assets/icons/` | Hand-drawn icons for silver, copper, oil and gas |
| `assets/blog/` | Blog cover images (SVG) |

## Things to know when editing

- **`landing.html` must follow `index.html`.** After changing `index.html`, regenerate it:
  ```bash
  python3 -c "s=open('index.html',encoding='utf8').read();b='\n'.join(s.split('\n')[1:]).rstrip();open('landing.html','w',encoding='utf8').write(b[:-len('</body></html>')].rstrip('\n')+'\n')"
  ```
- **Shared header, footer, menus and styles are copied into every page,** not included from one file. A change to them has to be made in each HTML file.
- **Blog pages are generated.** Edit `tools/build-blog.py`, not the `blog*.html` files, then rerun it.
- **Prices, charts and the 12 extra coins in the home coin picker are sample data,** not market data. The status page data and the terms text are drafts.
- **Restore point:** the tag `v1-full-home` is the site before the home page was reduced to the hero.
