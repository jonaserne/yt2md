# yt2md — YouTube → Markdown Library

A small, automation-first CLI that turns a list of YouTube URLs into:
- `.srt` captions (prefer YouTube captions if available)
- Whisper fallback transcription when captions are missing
- a clean `.md` transcript per video
- a simple `index.csv` for importing into Obsidian / NotebookLM / Docs workflows

## Features

- Input: `yt2md/input/sources.txt` or `yt2md/input/sources.csv`
- Output per video: `yt2md/output/<video_id>/`
  - `<video_id>.md`
  - captions `.srt` (YouTube or Whisper)
- Index: `yt2md/output/index.csv`
- Fallback: If YouTube captions fail or are missing, use Whisper (via `faster-whisper`)

## Project structure

yt2md/
configs/
default.yaml
input/
sources.txt
output/
src/yt2md/
cli.py
config.py
sources.py
youtube.py
whisper_fallback.py
srt_to_markdown.py
index.py


## Quickstart

1) Create venv + install

cd yt2md
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .

2) Add sources

Put one URL per line into:

yt2md/input/sources.txt

3) Run
yt2md



## Notes

YouTube may rate-limit subtitle downloads (HTTP 429). If that happens, retry later or reduce batch size.

Some YouTube extraction paths require a JS runtime for yt-dlp (you saw warnings). The pipeline can still work, but some formats may be missing.

## License / Usage

See LICENSE. If you want to use this code commercially or in another project, contact the author.
