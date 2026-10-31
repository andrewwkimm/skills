"""Prints the total size of the regular files under a directory and its five largest files."""

import sys
from pathlib import Path


def summarize(root: Path) -> tuple[int, list[tuple[Path, int]]]:
    """Returns the total bytes under root and the five largest files, largest first."""
    sizes = [(path, path.lstat().st_size) for path in root.rglob("*") if path.is_file() and not path.is_symlink()]
    largest = sorted(sizes, key=lambda item: item[1], reverse=True)[:5]
    return sum(size for _, size in sizes), largest


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: du.py DIRECTORY", file=sys.stderr)
        return 1
    root = Path(argv[1])
    try:
        total, largest = summarize(root)
    except OSError as error:
        print(f"du.py: {error}", file=sys.stderr)
        return 1
    print(total)
    for path, size in largest:
        print(f"{size}\t{path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
