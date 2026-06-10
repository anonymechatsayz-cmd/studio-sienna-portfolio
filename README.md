# Studio Sienna — Portfolio

Site portfolio statique (HTML/CSS/JS, Tailwind figé, images WebP optimisées).

## Déploiement (Vercel)
Le site déployable (`index.html` + `images/`) est **à la racine** du repo.

À l'import sur Vercel : laisser **tous les réglages par défaut**
(Root Directory = racine, Framework Preset = `Other`). Aucun build.

Chaque `git push` redéploie automatiquement.

## Modifier le design
1. Éditer la source `Portfolio.html` (Tailwind via CDN, pratique pour itérer).
2. Régénérer le CSS figé :
   `npx tailwindcss@3.4.17 -c _build/tailwind.config.js -i _build/input.css -o _build/tw.css --minify`
3. Régénérer `index.html` (Tailwind figé) : `python _build/make_dist.py`
4. `git add . && git commit && git push` → Vercel redéploie.

## Structure
- `index.html` — site déployé (Tailwind figé, généré depuis la source)
- `Portfolio.html` — source éditable (Tailwind via CDN)
- `images/*.webp` — captures optimisées (1,3 Mo au total)
- `_build/` — scripts de build (Tailwind, site, standalone, optimisation images)
