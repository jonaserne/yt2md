from pathlib import Path
from yt2md.config import BASE_DIR


def resolve_path(path_value: str) -> Path:
    """
    Wandelt einen Config-Pfad in einen absoluten Pfad um.
    Relative Pfade werden relativ zum Repo-Root interpretiert.
    """
    path = Path(path_value)

    if path.is_absolute():
        return path

    return BASE_DIR / path
