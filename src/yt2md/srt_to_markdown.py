from pathlib import Path
import re


TIMESTAMP_RE = re.compile(
    r"\d{2}:\d{2}:\d{2},\d{3}\s-->\s\d{2}:\d{2}:\d{2},\d{3}"
)


def srt_to_markdown(
    srt_path: Path,
    md_path: Path,
    title: str,
    source_url: str,
):
    """
    Wandelt SRT in ruhiges Markdown:
    - entfernt Zeitstempel & Nummern
    - fasst Zeilen zu Absätzen zusammen
    """

    lines = srt_path.read_text(encoding="utf-8").splitlines()

    text_lines: list[str] = []
    buffer: list[str] = []

    for line in lines:
        line = line.strip()

        if not line:
            if buffer:
                text_lines.append(" ".join(buffer))
                buffer = []
            continue

        if line.isdigit():
            continue

        if TIMESTAMP_RE.match(line):
            continue

        buffer.append(line)

    if buffer:
        text_lines.append(" ".join(buffer))

    # sehr kurze Fragmente zusammenziehen
    paragraphs: list[str] = []
    current = ""

    for line in text_lines:
        if len(current) < 300:
            current = f"{current} {line}".strip()
        else:
            paragraphs.append(current)
            current = line

    if current:
        paragraphs.append(current)

    md = []

    # --- Frontmatter ---
    md.append("---")
    md.append(f'title: "{title}"')
    md.append(f'source: "{source_url}"')
    md.append("type: transcript")
    md.append("---\n")

    # --- Inhalt ---
    md.append(f"# {title}\n")

    for p in paragraphs:
        md.append(p + "\n")

    md_path.write_text("\n".join(md), encoding="utf-8")

