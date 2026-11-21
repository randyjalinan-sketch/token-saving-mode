#!/usr/bin/env python3
"""PreToolUse hook untuk Read: PDF dikonversi ke Markdown dulu, lalu Markdown itu yang dibaca.

- Jika file yang dibaca berakhiran .pdf, konversi (pdftotext) disimpan di cache lock
  (lihat cache_lock.py). Konversi yang sama tidak diulang selama PDF-nya tidak berubah.
- Read pada PDF lalu ditolak dengan pesan berisi path .md, supaya Claude membaca .md itu.
- Jika konversi gagal, Read dibiarkan lewat (tidak memblokir pekerjaan).
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cache_lock  # noqa: E402


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (data.get("tool_input") or {}).get("file_path", "")
    if not fp.lower().endswith(".pdf"):
        return 0
    src = Path(fp)
    if not src.is_file():
        return 0

    md = cache_lock.get("pdf-md", str(src))
    if md is None:
        raw = Path(str(src) + ".txt.tmp")
        try:
            subprocess.run(
                ["pdftotext", "-layout", str(src), str(raw)],
                check=True, capture_output=True, timeout=300,
            )
            body = raw.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return 0
        finally:
            if raw.exists():
                raw.unlink()
        out = Path(str(src) + ".md.tmp")
        out.write_text(f"# {src.name}\n\nSumber: {src}\n\n{body}", encoding="utf-8")
        try:
            md = cache_lock.put("pdf-md", str(src), str(out))
        finally:
            out.unlink()

    reason = (
        f"PDF ini sudah dikonversi ke Markdown dan disimpan di cache: {md}. "
        "Baca file Markdown itu, bukan PDF-nya."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
