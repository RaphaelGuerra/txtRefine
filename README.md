# txtRefine — Philosophy Text Fixer

Last updated: 2026-01-23

## Table of Contents

<!-- TOC start -->
- [What It Does](#what-it-does)
- [How It Works](#how-it-works)
- [Run Locally](#run-locally)
- [Usage](#usage)
- [Configuration](#configuration)
- [Status & Learnings](#status--learnings)
- [License](#license)
<!-- TOC end -->

[![Lint](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/readme-lint.yml/badge.svg)](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/readme-lint.yml)
[![Security](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/security.yml/badge.svg)](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/security.yml)

Small utility that cleans up Portuguese philosophy texts by normalizing names and
terms (e.g., `Socrátes` → `Sócrates`, `aristoteles` → `Aristóteles`).

This is a portfolio side project focused on text‑cleanup UX and fast,
deterministic replacements. Not a production tool.

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

Run tests:

```bash
python3 -m unittest tests/test_term_matching.py
```

## Usage

```bash
# Interactive flow (prompts for input/output)
python main.py

# Direct refine with defaults (prints preview, asks to save)
python main.py --input input/my-text.txt --output output/my-text-clean.txt
```

## Configuration

Defaults can be provided via a JSON config file or environment variables.

Config search order:

1. `TXTREFINE_CONFIG` (explicit path)
2. `./txtrefine.json`
3. `~/.config/txtrefine/config.json`

Supported keys (config or env):

- `model` / `TXTREFINE_MODEL`
- `no_streaming` / `TXTREFINE_NO_STREAMING`
- `max_workers` / `TXTREFINE_MAX_WORKERS`
- `input` / `TXTREFINE_INPUT`
- `output` / `TXTREFINE_OUTPUT`

Example `txtrefine.json`:

```json
{
  "model": "llama3.2:latest",
  "no_streaming": true,
  "max_workers": 4
}
```

## Status & Learnings

- Functional prototype to explore text normalization and reviewable diffs
- Next ideas: term packs by era/school, CLI flags, and VS Code integration

## License

All rights reserved. Personal portfolio project — not for production use.
