from pathlib import Path
from yt_dlp import YoutubeDL


def download_audio(url: str, output_dir: Path) -> Path:
    """
    Lädt Audio als mp3 herunter (für Whisper).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": str(output_dir / "%(id)s"),
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return output_dir / f"{info['id']}.mp3"
