from pathlib import Path
import csv


def load_sources(input_dir: Path) -> list[str]:
    """
    Lädt YouTube-URLs aus sources.txt oder sources.csv.
    Gibt leere Liste zurück, wenn nichts vorhanden ist.
    """

    input_dir.mkdir(parents=True, exist_ok=True)

    txt_path = input_dir / "sources.txt"
    csv_path = input_dir / "sources.csv"

    # --------------------------------------------------
    # sources.txt
    # --------------------------------------------------
    if txt_path.exists():
        lines = [
            line.strip()
            for line in txt_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        return lines

    # --------------------------------------------------
    # sources.csv
    # --------------------------------------------------
    if csv_path.exists():
        urls = []
        with csv_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "url" not in reader.fieldnames:
                raise ValueError("sources.csv braucht eine Spalte 'url'")
            for row in reader:
                if row["url"].strip():
                    urls.append(row["url"].strip())
        return urls

    # --------------------------------------------------
    # nichts vorhanden → leere Vorlage anlegen
    # --------------------------------------------------
    txt_path.write_text(
        "# Eine YouTube-URL pro Zeile\n"
        "# Beispiel:\n"
        "# https://www.youtube.com/watch?v=XXXXXXXXXXX\n",
        encoding="utf-8",
    )

    print("Hinweis: input/sources.txt wurde angelegt – bitte URLs eintragen.")

    return []
