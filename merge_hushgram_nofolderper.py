
import os
import time
from pathlib import Path

SOURCES = [
    Path("/storage/emulated/0/Pictures/Instagram"),
    Path("/storage/emulated/0/Movies/Instagram"),
]

DESTINATION = Path("/storage/emulated/0/Download/HushGram")
STABILITY_WAIT = 2
LOG = Path.home() / "hushgram_move.log"


def log(message):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}"
    print(line)
    with LOG.open("a") as f:
        f.write(line + "\n")


def unique_target(target):
    """Generate an unused filename without overwriting existing files."""
    if not target.exists():
        return target

    counter = 1

    while True:
        candidate = target.with_name(
            f"{target.stem} ({counter}){target.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1


def move_contents(source, destination):
    destination.mkdir(parents=True, exist_ok=True)

    try:
        entries = list(source.iterdir())
    except OSError as e:
        log(f"Cannot read {source}: {e}")
        return

    for item in entries:
        target = destination / item.name

        if item.is_dir() and not item.is_symlink():
            if target.exists() and not target.is_dir():
                log(f"CONFLICT (folder vs file): {item}")
                continue

            target.mkdir(exist_ok=True)
            move_contents(item, target)

            try:
                item.rmdir()
                log(f"Removed empty folder: {item}")
            except OSError:
                pass

        elif item.is_file():
            try:
                before = item.stat()
                time.sleep(STABILITY_WAIT)
                after = item.stat()

                if (before.st_size, before.st_mtime_ns) != (
                    after.st_size,
                    after.st_mtime_ns,
                ):
                    log(f"Still changing; left in source: {item}")
                    continue

                # Rename incoming duplicates instead of skipping them.
                final_target = unique_target(target)

                os.rename(item, final_target)

                if final_target != target:
                    log(
                        f"RENAMED DUPLICATE: {item.name} "
                        f"-> {final_target.name}"
                    )
                else:
                    log(f"MOVED: {item} -> {final_target}")

            except FileNotFoundError:
                pass
            except OSError as e:
                log(f"ERROR moving {item}: {e}")


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)

    for source in SOURCES:
        if not source.is_dir():
            log(f"Source not found: {source}")
            continue

        log(f"Scanning: {source}")
        move_contents(source, DESTINATION)

    log("Scan complete.")


if __name__ == "__main__":
    main()
