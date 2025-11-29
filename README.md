# txtRefine — Philosophy Text Fixer

Last updated: 2025-11-29

## Table of Contents

<!-- TOC start -->
- [What It Does](#what-it-does)
- [How It Works](#how-it-works)
- [Run Locally](#run-locally)
- [Status & Learnings](#status-learnings)
- [License](#license)
<!-- TOC end -->

Small utility that cleans up Portuguese philosophy texts by normalizing names and terms (e.g., `Socrátes` → `Sócrates`, `aristoteles` → `Aristóteles`).

This is a portfolio side project focused on text‑cleanup UX and fast, deterministic replacements. Not a production tool.

## What It Does
- Detects and fixes common misspellings of philosopher names and key terms
- Preserves the rest of the text exactly as written
- Processes large files quickly

## How It Works
- Uses curated maps and fuzzy matching tuned for PT‑BR philosophy texts
- Produces a diff/preview of changes and a clean output file
- Stateless by default; can optionally cache frequent fixes

## Run Locally
Prerequisites: Python 3.10+

```bash
python main.py
```

Follow the prompts to choose your input file and review changes before saving.

## Status & Learnings
- Functional prototype to explore text normalization and reviewable diffs
- Next ideas: term packs by era/school, CLI flags, and VS Code integration

## License
All rights reserved. Personal portfolio project — not for production use.
