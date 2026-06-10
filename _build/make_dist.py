import pathlib

# Builds the deployable site AT THE REPO ROOT (index.html + images/*.webp),
# so Vercel's default config (Root Directory = repo root) serves it with zero setup.
root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "Portfolio.html").read_text(encoding="utf-8")
tw = (root / "_build" / "tw.css").read_text(encoding="utf-8")

# Freeze Tailwind (CDN runtime is not for production); keep Google Fonts <link>
# (standard + fast in prod) and keep images as external cacheable .webp files.
cdn = '<script src="https://cdn.tailwindcss.com"></script>'
assert cdn in html, "tailwind cdn tag not found"
html = html.replace(cdn, "<style>\n" + tw + "\n</style>")

(root / "index.html").write_text(html, encoding="utf-8")

# report
webps = sorted(p.name for p in (root / "images").glob("*.webp"))
print(f"[ok] index.html  ({(root/'index.html').stat().st_size/1024:.0f} KB) at repo root")
print(f"[check] cdn.tailwindcss in output: {'cdn.tailwindcss' in (root/'index.html').read_text(encoding='utf-8')}")
print(f"[check] images at root: {webps}")
