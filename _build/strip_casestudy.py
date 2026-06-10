import pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
p = root / "Portfolio.html"
html = p.read_text(encoding="utf-8")

# 1. Remove the dead "Étude de cas" anchor block on all 4 cards
pat = re.compile(
    r'\n[ \t]*<a href="#" class="arrow-link" style="color: var\(--terra-deep\)">.*?Étude de cas.*?</a>',
    re.S,
)
html, n1 = pat.subn('', html)

# 2. Promote "Voir le site" as the primary action (ink-60 -> terra-deep)
html, n2 = re.subn(
    r'class="arrow-link" style="color: var\(--ink-60\)"',
    'class="arrow-link" style="color: var(--terra-deep)"',
    html,
)

p.write_text(html, encoding="utf-8")
print(f"removed 'Étude de cas' blocks: {n1}  |  recolored 'Voir le site': {n2}")
print(f"remaining dead href=\"#\" in file: {html.count(chr(34)+'#'+chr(34))}")
