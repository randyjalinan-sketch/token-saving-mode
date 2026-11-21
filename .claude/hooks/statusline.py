#!/usr/bin/env python3
"""Status line: tampilkan model, folder, dan pemakaian konteks jika tersedia.

Claude Code mengirim JSON ke stdin. Field dibaca dengan aman; jika tidak ada, dilewati.
"""
import json
import sys
from pathlib import Path


def pick(d, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur if cur is not None else default


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    model = pick(data, "model", "display_name") or pick(data, "model", "id") or "model?"
    folder = Path(pick(data, "workspace", "current_dir") or pick(data, "cwd") or ".").name

    used = pick(data, "context_window", "used_percentage")
    ctx = f"ctx {used:.0f}%" if isinstance(used, (int, float)) else "ctx -"

    cost = pick(data, "cost", "total_cost_usd")
    cost_txt = f" | ${cost:.2f}" if isinstance(cost, (int, float)) else ""

    print(f"{model} | {folder} | {ctx}{cost_txt}")


if __name__ == "__main__":
    main()
