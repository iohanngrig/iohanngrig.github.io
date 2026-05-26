# iohanngrig.github.io

Personal research site of Hovhannes Grigoryan — built with [Quartz 4](https://quartz.jzhao.xyz).

## Status

**Local only.** Not yet deployed. Deployment gated on:
1. About page + CV content (T003)
2. Post #1 and Post #2 (T007, T008)
3. Privacy check passing (`scripts/privacy_check.py`)
4. Explicit deploy approval from hgrig

## Preview locally

```bash
cd iohanngrig.github.io
npx quartz build --serve
# → http://localhost:8080
```

The `--serve` flag starts a local dev server with hot-reload. Nothing is published.

## Deploy (WHEN APPROVED — not before)

When hgrig gives explicit approval to deploy, the deployment steps are:

```bash
# 1. Run privacy check — MUST pass
python3 scripts/privacy_check.py --strict

# 2. Initialize git if not already
git init -b v4
git add -A
git commit -m "Initial commit"

# 3. Add remote to GitHub Pages repo
git remote add origin git@github.com:iohanngrig/iohanngrig.github.io.git

# 4. Deploy via Quartz's built-in sync
npx quartz sync
```

## Privacy guardrails

See `.privacy/PRIVACY_PROTOCOL.md`. Amazon-confidential content MUST NOT appear on the public site. A pre-deploy privacy scanner enforces this.

## Structure

```
iohanngrig.github.io/
├── content/              # markdown pages (publicly rendered)
│   ├── index.md          # homepage (name + thesis)
│   ├── about.md          # about page (placeholder, T003)
│   └── writing.md        # posts index (placeholder)
├── quartz.config.ts      # site configuration
├── quartz.layout.ts      # layout / components
├── scripts/
│   └── privacy_check.py  # Amazon-confidentiality scanner
├── .privacy/
│   ├── patterns.txt      # banned patterns (case-insensitive)
│   └── PRIVACY_PROTOCOL.md
└── package.json
```
