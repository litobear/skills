---
name: google-slides-deck-builder
description: Build or update Google Slides decks from markdown outlines with rigorous structure (title, key points, speaker notes) using Google Slides API. Use when user asks to convert docs/sections into presentation slides, revise slide logic flow, or automate slide creation. Requires Slides API enabled and presentation shared to service account.
---

# Google Slides Deck Builder

Create professional slide decks from source docs with consistent structure and concise bullets.

## Preflight (must pass before editing slides)

1. Service account key exists (default):
   - `/home/ubuntu/.openclaw/workspace/.env.d/google-sa.json`
2. Google Slides API enabled for the service-account project.
3. Target presentation is shared as **Editor** to service-account email.
4. Python deps available in `.venv-gcal`:
   - `google-api-python-client`, `google-auth`

If any preflight item fails, prepare slide content locally and tell user exact unblock steps.

## Workflow

1. Identify source sections from markdown.
2. Build a slide outline with strict logic:
   - context → core concept → mechanism → comparison → implications → summary
3. Keep each slide concise:
   - title + 3–5 bullets
   - optional speaker notes
4. Apply deck updates via script:
   - `scripts/apply_slides_outline.py`
5. Report what was added/updated and any blockers.

## Script usage

```bash
/home/ubuntu/.openclaw/workspace/.venv-gcal/bin/python \
  /home/ubuntu/.openclaw/workspace/skills/google-slides-deck-builder/scripts/apply_slides_outline.py \
  --presentation-id <GOOGLE_SLIDES_ID> \
  --outline-json <path/to/outline.json> \
  --service-account /home/ubuntu/.openclaw/workspace/.env.d/google-sa.json
```

## Output standards

- Prefer Traditional Chinese for this workspace user.
- Keep technical precision; avoid hype language.
- Ensure terminology is consistent:
  - interactive proof / non-interactive proof
  - Fiat–Shamir transform
  - GKR
  - zk-SNARK
- Add one recap slide with actionable takeaways.
