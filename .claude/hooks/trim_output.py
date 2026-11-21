#!/usr/bin/env python3
"""PostToolUse hook: potong output yang terlalu panjang sebelum dikirim ke model.

Berlaku untuk Bash, Grep, Glob, WebFetch, Read, dan tool MCP (lihat matcher di settings.json).
Setiap string di dalam tool_response yang lebih dari TRIM_MAX_LINES baris dipotong jadi
awal + catatan + akhir.

Aturan khusus Read: jika pemanggilan sudah memakai offset atau limit (membaca sebagian
yang dipilih sendiri), tidak dipotong. Pemotongan hanya untuk pembacaan file penuh.

Env: TRIM_MAX_LINES (default 200), TRIM_KEEP (default 80 baris per sisi).
"""
import json
import os
import sys

MAX_LINES = int(os.environ.get("TRIM_MAX_LINES", "200"))
KEEP = int(os.environ.get("TRIM_KEEP", "80"))


def hint_for(tool):
    if tool == "Read":
        return "baca bagian tengah dengan offset dan limit"
    if tool == "Bash":
        return "pakai grep atau tail untuk bagian tengah"
    return "persempit pencarian untuk melihat bagian tengah"


def trim_text(text, tool):
    lines = text.splitlines()
    if len(lines) <= MAX_LINES:
        return text, 0
    dropped = len(lines) - 2 * KEEP
    note = f"... [{dropped} baris dipotong oleh hook trim_output; {hint_for(tool)}] ..."
    return "\n".join(lines[:KEEP] + [note] + lines[-KEEP:]), dropped


def trim_any(value, tool):
    """Kembalikan (nilai_baru, jumlah_baris_dibuang) secara rekursif."""
    if isinstance(value, str):
        return trim_text(value, tool)
    if isinstance(value, list):
        out, total = [], 0
        for item in value:
            v, d = trim_any(item, tool)
            out.append(v)
            total += d
        return out, total
    if isinstance(value, dict):
        out, total = {}, 0
        for k, item in value.items():
            v, d = trim_any(item, tool)
            out[k] = v
            total += d
        return out, total
    return value, 0


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}
    resp = data.get("tool_response")
    if resp is None:
        return 0

    # Read dengan offset atau limit: pembacaan sebagian yang disengaja, biarkan utuh.
    if tool == "Read" and isinstance(tool_input, dict) and (
        "offset" in tool_input or "limit" in tool_input
    ):
        return 0

    new, dropped = trim_any(resp, tool)
    if dropped == 0:
        return 0

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedToolOutput": new,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
