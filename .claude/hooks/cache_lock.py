#!/usr/bin/env python3
"""Cache lock: simpan hasil penting dan pakai ulang selama sumbernya tidak berubah.

Kunci = nama + sha256 isi sumber. Jika isi sumber berubah, kuncinya ikut berubah,
sehingga hasil lama otomatis tidak terpakai.

Pemakaian (CLI):
  cache_lock.py get  <nama> <file_sumber>                  -> cetak path hasil; exit 1 jika belum ada
  cache_lock.py put  <nama> <file_sumber> <file_hasil>     -> simpan hasil, cetak path
  cache_lock.py path <nama> <file_sumber>                  -> cetak path hasil (tanpa cek ada/tidak)
Lokasi cache: $CLAUDE_CACHE_DIR, default ~/.claude/cache
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

CACHE = Path(os.environ.get("CLAUDE_CACHE_DIR", Path.home() / ".claude" / "cache"))


def source_hash(src: str) -> str:
    h = hashlib.sha256()
    with open(src, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def locked_path(name: str, src: str) -> Path:
    return CACHE / name / f"{source_hash(src)[:32]}.out"


def get(name: str, src: str):
    p = locked_path(name, src)
    return p if p.exists() else None


def put(name: str, src: str, result: str) -> Path:
    p = locked_path(name, src)
    p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(result, p)
    return p


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    cmd, name, src = argv[0], argv[1], argv[2]
    if cmd == "get":
        p = get(name, src)
        if p is None:
            return 1
        print(p)
        return 0
    if cmd == "put" and len(argv) == 4:
        print(put(name, src, argv[3]))
        return 0
    if cmd == "path":
        print(locked_path(name, src))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
