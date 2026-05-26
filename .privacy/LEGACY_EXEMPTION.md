# Legacy site archive — privacy exemption rationale

**Path:** `quartz/static/legacy/`
**Source:** snapshot of the original `iohanngrig/iohanngrig.github.io` `main` branch as of 2026-05-26
**Original publication date:** 2019-2020 (per content); first GitHub Pages publish ~2024-02-01 per HTTP `last-modified` header
**Privacy status:** EXEMPT from the privacy-check scanner (`scripts/privacy_check.py`)

## Why exempt

The legacy content predates the user's Amazon employment (started August 2024) by 4+ years. It has been continuously public on `iohanngrig.github.io` since at least early 2020. By construction it cannot contain Amazon-confidential references — there was nothing to leak.

A literal scan of the legacy folder against the privacy patterns in `.privacy/patterns.txt` returns 163 false-positive hits, all of which are confirmed harmless:

- **`MARS`** (162 hits) — Font Awesome 4.x gender-symbol icon CSS classes (`.fa-mars`, `.fa-mars-double`, `.fa-venus-mars`, `.fa-mars-stroke-*`). These are the Mars/Venus astronomical symbols used as gender icons in the Font Awesome 4.x library, embedded by Jupyter `nbconvert` as part of standard notebook styling. Not Amazon's MARS project.
- **`CCOA`** (~17 hits) — random 4-letter substrings inside base64-encoded PNG image data URIs (Jupyter notebook output figures). Not Amazon's CCOA system.
- **`PVE`, `CCF`** (~5 hits) — same: random substrings in base64-encoded image data.
- **`OPS`** (~1 hit) — appears in the literal string `tensorflow.python.ops.array_ops` inside a runtime warning printed by an old TensorFlow notebook. Not Amazon's OPS metric.
- **`JFK*`, `BWI*`, etc.** — the airport-code prefix of Amazon building IDs (JFK27, JFK36, BWI17) is a 3-letter sequence that appears at random in base64 strings. A scan finds `JFK0`, `JFK11`, `JFK67`, `JFK82` etc. — all base64 noise, not real building references.

## Manual verification performed

A targeted search for genuine Amazon-employment-era markers was run on 2026-05-26 and returned **zero matches**:

| Search | Result |
|---|---|
| `amazon.com`, `amzn-aws`, `@amazon`, `aws.dev`, `a2z.com` | 0 matches |
| Internal aliases: `tessacd`, `cmbeau`, `kevnche`, `defimov`, `abhigpta` | 0 matches |
| Project codenames: `BDAgent`, `CCOA` (literal phrase, not base64), `MARS Agent` (literal phrase), `CreatorScience`, `creator-economics` | 0 matches |
| Job-context phrases: `Senior Applied Scientist`, `Amazon Creators`, `Creator Rewards` | 0 matches |

## Operational rule

- **`scripts/privacy_check.py`** scans `content/` by default, and `--strict` adds top-level repo MD files. It does NOT scan `quartz/static/legacy/`. This is intentional. The CI workflow in `.github/workflows/deploy.yml` invokes the default scan only.
- If new content is added to the legacy folder later (it shouldn't be, but if), re-do the manual targeted search above before pushing.
- If the privacy patterns in `.privacy/patterns.txt` change, the legacy folder's exemption is re-justified by the four-year time gap, not by the specific patterns. New patterns added in the future cannot apply retroactively to 2019 content.
