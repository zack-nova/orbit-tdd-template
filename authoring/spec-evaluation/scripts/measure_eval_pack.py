#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

try:
    import tiktoken
except ImportError as exc:
    raise SystemExit(
        "tiktoken is required. Run via: uvx --from tiktoken python "
        "authoring/scripts/measure_eval_pack.py ..."
    ) from exc


def parse_args():
    parser = argparse.ArgumentParser(
        description="Measure pack-based static metrics for README comparison rows."
    )
    parser.add_argument("--pack-dir", required=True, help="Path to one eval pack directory.")
    parser.add_argument(
        "--tokenizer",
        default="o200k_base",
        help="tiktoken encoding name. Default: o200k_base",
    )
    return parser.parse_args()


def format_k(tokens):
    return f"{round(tokens / 1000.0, 1):.1f}k"


def main():
    args = parse_args()
    pack_dir = Path(args.pack_dir).resolve()
    pack = json.loads((pack_dir / "pack.json").read_text())
    files_root = pack_dir / "files"
    enc = tiktoken.get_encoding(args.tokenizer)

    rows = []
    total = 0
    max_path = None
    max_tokens = -1
    for relpath in pack["allowed_files"]:
        content = (files_root / relpath).read_text()
        tokens = len(enc.encode(content))
        rows.append({"path": relpath, "tokens": tokens})
        total += tokens
        if tokens > max_tokens:
            max_tokens = tokens
            max_path = relpath

    result = {
        "row_id": pack["row_id"],
        "spec_display": pack["spec_display"],
        "source_kind": pack["source_kind"],
        "source_repo": pack["source_repo"],
        "source_commit": pack.get("source_commit"),
        "source_commit_pinned": pack.get("source_commit_pinned", False),
        "tokenizer": args.tokenizer,
        "static_file_count": len(pack["allowed_files"]),
        "static_file_tokens": rows,
        "static_load_tokens": total,
        "static_load_display": format_k(total),
        "max_file": {
            "path": max_path,
            "tokens": max_tokens,
            "display": format_k(max_tokens),
        },
        "missing_files": pack.get("missing_files", []),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
