import base64, re, urllib.request, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "Portfolio.html").read_text(encoding="utf-8")
twcss = (root / "_build" / "tw.css").read_text(encoding="utf-8")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

def fetch(url, decode=True):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=60).read()
    return data.decode("utf-8") if decode else data

# --- 1. Inline the 4 project screenshots as base64 -------------------------
names = ["maths-ultime", "jardin-ditalie", "la-toiletterie", "au-temps-du-froment"]
for name in names:
    raw = (root / "images" / f"{name}.webp").read_bytes()
    uri = "data:image/webp;base64," + base64.b64encode(raw).decode()
    before = html
    html = html.replace(f"url('images/{name}.webp')", f"url('{uri}')")
    assert html != before, f"image ref not found: {name}"
print("[ok] 4 images inlined")

# --- 2. Freeze Tailwind: replace CDN script with the compiled static CSS ----
cdn = '<script src="https://cdn.tailwindcss.com"></script>'
assert cdn in html, "tailwind cdn script tag not found"
html = html.replace(cdn, "<style>\n" + twcss + "\n</style>")
print("[ok] tailwind frozen")

# --- 3. Inline Google Fonts (@font-face + woff2 as base64) ------------------
fonts_url = ("https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700"
             "&family=JetBrains+Mono:wght@400;500&display=swap")
try:
    css = fetch(fonts_url)
    woff_urls = sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", css)))
    cache = {}
    for u in woff_urls:
        cache[u] = "data:font/woff2;base64," + base64.b64encode(fetch(u, decode=False)).decode()
    css = re.sub(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)",
                 lambda m: "url(" + cache[m.group(1)] + ")", css)
    # swap the <link> for the fully inlined @font-face block
    link_pat = r'<link href="https://fonts\.googleapis\.com/css2[^>]*>'
    assert re.search(link_pat, html), "google fonts link not found"
    html = re.sub(link_pat, "<style>\n" + css + "\n</style>", html, count=1)
    # preconnect hints are now useless -> drop them (harmless either way)
    html = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", html)
    print(f"[ok] fonts inlined ({len(woff_urls)} woff2 files)")
except Exception as e:
    print(f"[WARN] font inline failed ({e}); keeping Google Fonts link", file=sys.stderr)

# --- 4. Write the standalone file ------------------------------------------
out = root / "Portfolio-autonome.html"
out.write_text(html, encoding="utf-8")

# --- 5. Verify no external runtime deps remain -----------------------------
leftovers = re.findall(r'(https?://[^\s"\')]+)', html)
critical = [u for u in leftovers if any(d in u for d in
            ("cdn.tailwindcss.com", "fonts.googleapis.com", "fonts.gstatic.com"))]
print(f"[done] wrote {out.name}  ({out.stat().st_size/1_000_000:.1f} MB)")
print(f"[check] remaining critical external refs: {len(critical)}")
for u in critical[:10]:
    print("   -", u)
