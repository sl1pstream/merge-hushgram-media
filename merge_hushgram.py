#!/usr/bin/env python3

import os
import time
from pathlib import Path

SOURCES = [
    Path("/storage/emulated/0/Pictures/Instagram"),
    Path("/storage/emulated/0/Movies/Instagram"),
]

DESTINATION = Path("/storage/emulated/0/Download/HushGram")
STABLE_AGE = 2  # seconds since last write before a file counts as finished
LOG = Path.home() / "hushgram_move.log"


def log(fh, message):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}"
    print(line)
    fh.write(line + "\n")
    fh.flush()


def unique_name(name, taken):
    """Return a name not already used in the destination, and reserve it."""
    if name not in taken:
        taken.add(name)
        return name

    stem, suffix = os.path.splitext(name)
    counter = 1

    while True:
        candidate = f"{stem} ({counter}){suffix}"

        if candidate not in taken:
            taken.add(candidate)
            return candidate

        counter += 1


def move_contents(source, destination, fh, stats, is_source_root=False):
    destination.mkdir(parents=True, exist_ok=True)

    try:
        taken = set(os.listdir(destination))
    except OSError as e:
        log(fh, f"Cannot list {destination}: {e}")
        return

    try:
        entries = list(os.scandir(source))
    except OSError as e:
        log(fh, f"Cannot read {source}: {e}")
        return

    for entry in entries:
        target = destination / entry.name

        # Ignore loose files in the original source directories.
        if is_source_root and entry.is_file():
            log(fh, f"IGNORED loose file: {entry.path}")
            continue

        try:
            if entry.is_dir(follow_symlinks=False):
                if entry.name in taken and not target.is_dir():
                    log(fh, f"CONFLICT (folder vs file): {entry.path}")
                    continue

                target.mkdir(exist_ok=True)
                taken.add(entry.name)
                move_contents(Path(entry.path), target, fh, stats)

                try:
                    os.rmdir(entry.path)
                    log(fh, f"Removed empty folder: {entry.path}")
                except OSError:
                    pass

            elif entry.is_file():
                st = entry.stat()

                # No sleep: only skip files still being written right now.
                if time.time() - st.st_mtime < STABLE_AGE:
                    stats["skipped"] += 1
                    log(fh, f"Still changing; left in source: {entry.path}")
                    continue

                # Rename incoming duplicates instead of skipping them.
                final_name = unique_name(entry.name, taken)
                final_target = destination / final_name

                os.rename(entry.path, final_target)
                stats["moved"] += 1

                if final_name != entry.name:
                    log(
                        fh,
                        f"RENAMED DUPLICATE: {entry.name} "
                        f"-> {final_name}",
                    )
                else:
                    log(fh, f"MOVED: {entry.path} -> {final_target}")

        except FileNotFoundError:
            pass
        except OSError as e:
            stats["errors"] += 1
            log(fh, f"ERROR moving {entry.path}: {e}")


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    stats = {"moved": 0, "skipped": 0, "errors": 0}
    started = time.time()

    with LOG.open("a") as fh:
        for source in SOURCES:
            if not source.is_dir():
                log(fh, f"Source not found: {source}")
                continue

            log(fh, f"Scanning: {source}")
            move_contents(source, DESTINATION, fh, stats, is_source_root=True)

        elapsed = time.time() - started
        count = stats["moved"]
        noun = "file" if count == 1 else "files"
        log(
            fh,
            f"Scan complete. Moved {count} {noun} in "
            f"{elapsed:.2f}s (skipped {stats['skipped']}, "
            f"errors {stats['errors']})",
        )


if __name__ == "__main__":
    main()
