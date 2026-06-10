import pathlib

# Builds the deployable site AT THE REPO ROOT (index.html, contact.html + images/*.webp),
# so Vercel's default config (Root Directory = repo root) serves it with zero setup.
root = pathlib.Path(__file__).resolve().parent.parent
tw = (root / "_build" / "tw.css").read_text(encoding="utf-8")
cdn = '<script src="https://cdn.tailwindcss.com"></script>'

# (source file with Tailwind CDN)  ->  (deployed file with frozen Tailwind)
PAGES = [
    ("Portfolio.html",   "index.html"),
    ("contact-src.html", "contact.html"),
]

for src, out in PAGES:
    html = (root / src).read_text(encoding="utf-8")
    assert cdn in html, f"tailwind cdn tag not found in {src}"
    # Freeze Tailwind (CDN runtime is not for production); Google Fonts <link> and
    # external .webp images are kept (standard + fast in prod).
    html = html.replace(cdn, "<style>\n" + tw + "\n</style>")
    (root / out).write_text(html, encoding="utf-8")
    has_cdn = "cdn.tailwindcss" in (root / out).read_text(encoding="utf-8")
    print(f"[ok] {out:14} ({(root/out).stat().st_size/1024:.0f} KB)  cdn-left:{has_cdn}")

webps = sorted(p.name for p in (root / "images").glob("*.webp"))
print(f"[check] images at root: {webps}")
