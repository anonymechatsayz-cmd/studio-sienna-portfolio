import pathlib
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent
img_dir = root / "images"
MAX_W = 1280          # 2x the ~640px card width -> sharp on retina
QUALITY = 82

names = ["maths-ultime", "jardin-ditalie", "la-toiletterie", "au-temps-du-froment"]
total_before = total_after = 0

for name in names:
    src = img_dir / f"{name}.png"
    dst = img_dir / f"{name}.webp"
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > MAX_W:
        im = im.resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    b, a = src.stat().st_size, dst.stat().st_size
    total_before += b; total_after += a
    print(f"{name:22} {w}x{h} {b/1_000_000:5.1f}MB  ->  {im.size[0]}x{im.size[1]} {a/1_000:6.0f}KB")

print(f"\nTOTAL {total_before/1_000_000:.1f} MB  ->  {total_after/1_000_000:.2f} MB")

# update source HTML references .png -> .webp
html_path = root / "Portfolio.html"
html = html_path.read_text(encoding="utf-8")
for name in names:
    html = html.replace(f"images/{name}.png", f"images/{name}.webp")
html_path.write_text(html, encoding="utf-8")
print("[ok] Portfolio.html references updated to .webp")
