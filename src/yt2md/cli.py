from pathlib import Path

from yt2md.config import load_config
from yt2md.sources import load_sources
from yt2md.youtube import (
    get_video_metadata,
    download_captions,
    download_audio,
)
from yt2md.whisper_fallback import transcribe_with_whisper
from yt2md.srt_to_markdown import srt_to_markdown
from yt2md.index import write_index


def main():
    # ------------------------------------------------------------
    # 1. Konfiguration & Pfade
    # ------------------------------------------------------------
    config = load_config()

    input_dir = Path(config["paths"]["input"])
    output_dir = Path(config["paths"]["output"])
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Suche Quellen in: {input_dir.resolve()}")

    # ------------------------------------------------------------
    # 2. Quellen laden
    # ------------------------------------------------------------
    sources = load_sources(input_dir)
    if not sources:
        print("Keine Quellen gefunden.")
        return

    index_entries: list[dict] = []

    # ------------------------------------------------------------
    # 3. Verarbeitung pro Video
    # ------------------------------------------------------------
    for url in sources:
        print("\n" + "-" * 60)

        # --- Metadaten ---
        meta = get_video_metadata(url)
        video_id = meta["id"]
        title = meta["title"]

        print(title)
        print(f"ID: {video_id}")

        video_dir = output_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        srt_path = None
        transcript_source = "youtube"

        # --------------------------------------------------------
        # 3a. YouTube-Captions
        # --------------------------------------------------------
        try:
            print("Versuche YouTube-Captions …")
            srt_path = download_captions(url, video_dir)
        except Exception as e:
            print(f"YouTube-Captions fehlgeschlagen: {e}")

        # --------------------------------------------------------
        # 3b. Whisper-Fallback
        # --------------------------------------------------------
        if not srt_path or not srt_path.exists():
            print("→ Fallback: Whisper")

            audio_path = download_audio(url, video_dir)

            srt_path = transcribe_with_whisper(
                audio_path=audio_path,
                output_dir=video_dir,
                language="en",
                model_size="base",
            )

            transcript_source = "whisper"
            print(f"SRT bereit (Whisper): {srt_path}")
        else:
            print(f"SRT bereit: {srt_path}")

        # --------------------------------------------------------
        # 3c. SRT → Markdown
        # --------------------------------------------------------
        md_path = video_dir / f"{video_id}.md"

        srt_to_markdown(
            srt_path=srt_path,
            md_path=md_path,
            title=title,
            source_url=url,
        )

        print(f"Markdown bereit: {md_path}")

        # --------------------------------------------------------
        # 3d. Index-Eintrag
        # --------------------------------------------------------
        index_entries.append(
            {
                "video_id": video_id,
                "title": title,
                "url": url,
                "markdown_path": str(md_path),
                "srt_path": str(srt_path),
                "transcript_source": transcript_source,
                "language": "en",
            }
        )

    # ------------------------------------------------------------
    # 4. Index schreiben
    # ------------------------------------------------------------
    write_index(index_entries, output_dir)
    print(f"\nIndex geschrieben: {output_dir / 'index.csv'}")

    print("\nFertig.")


if __name__ == "__main__":
    main()
