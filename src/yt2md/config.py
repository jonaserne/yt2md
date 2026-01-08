from pathlib import Path
import yaml

# Basisverzeichnis des Projekts (Repo-Root)
BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_CONFIG_PATH = BASE_DIR / "configs" / "default.yaml"


def load_config(path: Path | None = None) -> dict:
    config_path = path or DEFAULT_CONFIG_PATH

    if not config_path.exists():
        raise FileNotFoundError(f"Config nicht gefunden: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
