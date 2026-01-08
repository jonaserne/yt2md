from pathlib import Path
import subprocess
import json

from yt_dlp import YoutubeDL


# ------------------------------------------------------------
# Metadaten
# ------------------------------------------------------------
def get_video_metadata(url: str) -> dict:
    """
    Holt minimale Metadaten (ID, Titel) ohne Download
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "id": info["id"],
        "title": info.get("title", info["id"]),
    }


# ------------------------------------------------------------
# YouTube Captions → SRT
# ------------------------------------------------------------
def download_captions(url: str, output_dir: Path) -> Path | None:
    """
    Versucht, YouTube-Untertitel (manuell oder auto) als SRT zu laden.
    Gibt Pfad zur SRT zurück oder None.
    """

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "srt",
        "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
        "no_warnings": True,
        "quiet": True,
        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]

    srt_path = output_dir / f"{video_id}.en.srt"
    if srt_path.exists():
        return srt_path

    return None


# ------------------------------------------------------------
# Audio-Download für Whisper
# ------------------------------------------------------------
def download_audio(url: str, output_dir: Path) -> Path:
    """
    Lädt Audio als WAV für Whisper
    """

    audio_path = output_dir / "audio.wav"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "audio.%(ext)s"),
        "quiet": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    if not audio_path.exists():
        raise RuntimeError("Audio-Download fehlgeschlagen")

    return audio_path
