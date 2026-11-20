"""Write the 20 November 2026 world-news front page to the output dir.

The entry image is bundled in this repository as entry.png; this program
copies it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Standard library only, no network, deterministic output.
"""

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(SOURCE.read_bytes())
    want = digest(SOURCE)
    got = digest(target)
    if got != want:
        print(f"ERROR: sha256 mismatch: wrote {got}, expected {want}")
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes) sha256 {got}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
