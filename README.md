# Studio Sienna — Portfolio

Site portfolio statique (HTML/CSS/JS, Tailwind figé, images WebP optimisées).

## Déploiement (Vercel)
Le site déployable se trouve dans **`dist/`** (`index.html` + `images/`).

À l'import du repo sur Vercel :
- **Root Directory** = `dist`
- **Framework Preset** = `Other` (site statique, aucun build)

Chaque `git push` redéploie automatiquement.

## Modifier le design
1. Éditer la source `Portfolio.html` (Tailwind via CDN, pratique pour itérer).
2. Régénérer le CSS figé :
   `npx tailwindcss@3.4.17 -c _build/tailwind.config.js -i _build/input.css -o _build/tw.css --minify`
3. Reconstruire le dossier déployable : `python _build/make_dist.py`
4. `git add . && git commit && git push` → Vercel redéploie.

## Structure
- `dist/` — site déployé (Tailwind figé, WebP)
- `Portfolio.html` — source éditable
- `images/*.webp` — captures optimisées (1,3 Mo au total)
- `_build/` — scripts de build (Tailwind, dist, standalone, optimisation images)
