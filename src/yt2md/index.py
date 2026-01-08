from pathlib import Path
import csv
import json


def write_index(entries: list[dict], output_dir: Path):
    """
    Schreibt index.csv und index.json in das Output-Verzeichnis.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "index.csv"
    json_path = output_dir / "index.json"

    # -----------------------
    # CSV
    # -----------------------
    if entries:
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=entries[0].keys())
            writer.writeheader()
            writer.writerows(entries)

    # -----------------------
    # JSON
    # -----------------------
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

