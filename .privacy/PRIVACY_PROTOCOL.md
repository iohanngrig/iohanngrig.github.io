# Privacy Protocol — iohanngrig.github.io

**Last updated:** 2026-04-25
**Purpose:** Prevent any Amazon-confidential content from reaching the public site at any stage.

## The rule

Nothing in `content/`, `quartz.config.ts`, `quartz.layout.ts`, or any other file that ends up in the built site may reference:

- Amazon internal project names (MARS, BDAgentV2, CCOA, CCF, DRAM, CLV, IOHMM, PAP, MIP, SCUPED-internal details, etc.)
- Amazon internal terminology (GCCP, SOPS, iE%GCCP, gccp_sops_ratio, tier_target, compshop, etc.)
- Amazon-internal URLs (w.amazon.com, quip-amazon.com, code.amazon.com, phonetool, etc.)
- Amazon colleagues by alias or name except in rare public-by-default contexts (e.g., cited academic co-authors).
- Specific Amazon ticket IDs (P-numbers, CR-numbers, CSA-numbers, SIM issues).
- Specific Amazon dollar figures, creator counts, store counts, or marketplace codes.
- Direct quotes from internal Amazon documents (Quip, wiki, Forte).

The full banned-pattern list lives in `.privacy/patterns.txt`.

## The gate

Every build / preview / deploy must first pass:

```
python3 scripts/privacy_check.py
```

Exit code 0 = safe. Non-zero = banned content found. Fix before proceeding.

Run it with `--strict` to also scan repo-root markdown files:

```
python3 scripts/privacy_check.py --strict
```

## What IS safe to publish

- Hovhannes Grigoryan's name, title ("Senior Applied Scientist at Amazon"), NYC location.
- Physics PhD, physics publications (arXiv, journal links).
- Physics postdoc institutions (as listed on public CV).
- The locked research thesis: *"Causal identification and mechanism design for agent-driven decision systems."*
- General methodology (causal inference, DML, causal forests, mechanism design) without Amazon-specific application details.
- Open-source code releases once Amazon clearance has been obtained (e.g., SCUPED after T006).
- Published papers that have already been made public (AMLC title + venue is fine once paper is externally released; internal-only details stay internal).
- Physics-to-AI transition narrative, general (no specific Amazon project names).

## What to do when writing a new post

1. Draft locally in `content/writing/<post-slug>.md`.
2. Before previewing: `python3 scripts/privacy_check.py`.
3. Self-review: does this post require NDA to understand, or is every fact derivable from public sources?
4. If the post *applies* public research to Amazon work, describe the public methodology and use **synthetic or public benchmark data** for illustrations. Never paste internal figures.
5. Before deploying: `python3 scripts/privacy_check.py` passes (required) AND manual read-through (required).

## Escalation

If you are unsure whether a phrase is Amazon-confidential:

- Default to "yes, confidential" and rewrite it out.
- When in doubt, ask the coach or a Principal AS before the content goes public.
- The internal `Amazon Confidentiality Agreement` applies. PR/FAQs, 6-pagers, Quip docs, wiki entries, Forte reviews, and all Slack messages are NON-public.

## For the coach agent

The coach (career-coach.md) must treat the privacy protocol as a hard constraint. Any task that would produce public content (T007 post, T008 post, T012 CCF paper on public data, T013 CCF blog, T014 SCUPED companion) must include a step "run privacy_check.py before publishing" and must not output Amazon-internal identifiers in drafts.
