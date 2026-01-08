from pathlib import Path

from faster_whisper import WhisperModel


def transcribe_with_whisper(
    audio_path: Path,
    output_dir: Path,
    language: str = "en",
    model_size: str = "base",
) -> Path:
    """
    Transkribiert Audio mit Whisper (CPU-sicher).
    Gibt Pfad zur erzeugten SRT zurück.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    srt_path = output_dir / f"{audio_path.stem}.srt"

    # ------------------------------------------------------------
    # CPU-sichere Initialisierung (kein float16!)
    # ------------------------------------------------------------
    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",  # <- entscheidend für Mac / CPU
    )

    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
    )

    # ------------------------------------------------------------
    # SRT schreiben
    # ------------------------------------------------------------
    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with srt_path.open("w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            f.write(f"{i}\n")
            f.write(f"{fmt(seg.start)} --> {fmt(seg.end)}\n")
            f.write(seg.text.strip() + "\n\n")

    return srt_path
