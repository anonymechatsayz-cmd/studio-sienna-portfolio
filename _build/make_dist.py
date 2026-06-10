import pathlib, shutil

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "Portfolio.html").read_text(encoding="utf-8")
tw = (root / "_build" / "tw.css").read_text(encoding="utf-8")

# Freeze Tailwind (CDN runtime is not for production); keep Google Fonts <link>
# (standard + fast for a live site) and keep images as external cacheable files.
cdn = '<script src="https://cdn.tailwindcss.com"></script>'
assert cdn in html, "tailwind cdn tag not found"
html = html.replace(cdn, "<style>\n" + tw + "\n</style>")

dist = root / "dist"
if dist.exists():
    shutil.rmtree(dist)
(dist / "images").mkdir(parents=True)
(dist / "index.html").write_text(html, encoding="utf-8")
for p in sorted((root / "images").glob("*.webp")):
    shutil.copy(p, dist / "images" / p.name)

# report
total_img = sum(f.stat().st_size for f in (dist / "images").glob("*.webp"))
print(f"[ok] dist/index.html  ({(dist/'index.html').stat().st_size/1024:.0f} KB)")
print(f"[ok] dist/images/     ({len(list((dist/'images').glob('*.webp')))} files, {total_img/1_000_000:.2f} MB)")
print(f"[check] cdn.tailwindcss in output: {'cdn.tailwindcss' in (dist/'index.html').read_text(encoding='utf-8')}")
