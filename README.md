# txtRefine — PT-BR Transcript Refiner

Last updated: 2026-04-05

## Table of Contents

<!-- TOC start -->
- [What It Does](#what-it-does)
- [How It Works](#how-it-works)
- [Run Locally](#run-locally)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Status](#status)
- [License](#license)
<!-- TOC end -->

[![Lint](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/readme-lint.yml/badge.svg)](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/readme-lint.yml)
[![Security](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/security.yml/badge.svg)](https://github.com/RaphaelGuerra/txtRefine/actions/workflows/security.yml)

Small utility that turns rough transcript text into a cleaner, readable PT-BR transcript.
It is designed for text exported from audio recordings such as voice memos, meetings,
and interviews. v1 does not transcribe audio files directly.

## What It Does

- Cleans timestamps, common noise markers, spacing issues, and obvious ASR mistakes
- Fixes a small set of common PT-BR transcript and product-name errors
- Preserves meaning, chronology, and spoken tone while improving readability
- Works locally with deterministic cleanup plus optional Ollama polishing

## How It Works

- Applies conservative deterministic cleanup before the model runs
- Uses Ollama to improve punctuation, capitalization, and paragraph breaks
- Falls back to deterministic cleanup if the model is unavailable or over-shortens the text
- Keeps the current CLI workflow focused on `.txt` transcript input and cleaned `.txt` output

## Run Locally

Prerequisites: Python 3.10+

```bash
./txtrefine
```

On the first run, `./txtrefine` creates `.venv/` and installs the Python dependency automatically.
After that, the command stays available without manual activation.
Follow the prompts to choose a transcript file and review the cleaned output.

## Usage

```bash
# Recommended interactive flow
./txtrefine

# If you already activated your own venv, this also works
python3 main.py

# Direct refine with defaults
./txtrefine --input input/raw-transcript.txt --output output/refined-raw-transcript.txt

# Process every transcript in input/
./txtrefine --process-all
```

## Configuration

Defaults can be provided via a JSON config file or environment variables.

Config search order:

1. `TXTREFINE_CONFIG` (explicit path)
2. `./txtrefine.json`
3. `~/.config/txtrefine/config.json`

Supported keys:

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

## Testing

```bash
python3 -m unittest discover -s tests
```

## Status

- Current focus: readable PT-BR transcript cleanup for voice-memo style text
- Not in scope for this version: direct audio transcription, diarization, and summaries
- Future ideas: style presets, domain-specific correction packs, and transcript review diffs

## License

All rights reserved. Personal portfolio project.
