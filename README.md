# iohanngrig.github.io

Personal research site of Hovhannes Grigoryan — built with [Quartz 4](https://quartz.jzhao.xyz).

Live at: <https://iohanngrig.github.io/>
Old site (2019 archive): <https://iohanngrig.github.io/legacy/>

## Local preview

```bash
cd iohanngrig.github.io
npx quartz build --serve
# → http://localhost:8080
```

For a full production-style build (Quartz + legacy reposition):

```bash
npm run build
```

## Deploy

Pushes to the `v4` branch trigger `.github/workflows/deploy.yml`, which:

1. Runs `python3 scripts/privacy_check.py --strict` (build fails on any banned-pattern hit in `content/`)
2. Runs `npm run build` (= `bash scripts/build.sh`, which is `npx quartz build` then repositions `public/static/legacy/` → `public/legacy/`)
3. Verifies `public/legacy/index.html` and `public/index.html` both exist
4. Uploads `public/` as a Pages artifact and deploys

GitHub Pages is configured to deploy from "GitHub Actions" (Settings → Pages → Source).

## Privacy guardrails

- `.privacy/PRIVACY_PROTOCOL.md` — site-level protocol for Amazon-confidential content
- `.privacy/patterns.txt` — banned patterns scanned by `scripts/privacy_check.py`
- `.privacy/LEGACY_EXEMPTION.md` — rationale for exempting `quartz/static/legacy/` from the scan (content predates Amazon employment by 4+ years; all 163 raw matches are confirmed false positives in Font Awesome CSS / base64 image data)

## Structure

```
iohanngrig.github.io/
├── content/                      # markdown sources (Quartz processes these)
│   ├── index.md                  # homepage
│   ├── about.md                  # about page
│   ├── writing/                  # long-form essays
│   ├── lectures/                 # textbook chapters (Quarto-rendered)
│   ├── research-notes/           # short technical notes
│   └── applications/             # demo applications
├── quartz/                       # Quartz source (mostly upstream)
│   └── static/
│       └── legacy/               # 2019 archive (snapshot of old QuantMachine site)
├── quartz.config.ts              # site configuration
├── quartz.layout.ts              # layout / components
├── scripts/
│   ├── build.sh                  # production build wrapper
│   └── privacy_check.py          # Amazon-confidentiality scanner
├── .github/workflows/
│   └── deploy.yml                # GitHub Pages deploy (triggers on push to v4)
└── .privacy/                     # privacy guardrails
```
