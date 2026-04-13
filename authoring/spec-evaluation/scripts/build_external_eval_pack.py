#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build normalized external eval packs from a local reference snapshot."
    )
    parser.add_argument(
        "--config",
        default="authoring/readme/reference-comparison-config.json",
        help="Path to the external reference comparison config.",
    )
    parser.add_argument(
        "--snapshot-root",
        default="references/repo-docs-latest",
        help="Root containing fetched reference snapshots.",
    )
    parser.add_argument(
        "--out-root",
        default="authoring/eval-packs",
        help="Destination root for generated eval packs.",
    )
    parser.add_argument(
        "--row-id",
        help="Only build one row from the config.",
    )
    return parser.parse_args()


def repo_dir(repo_slug):
    return repo_slug.replace("/", "__")


def load_config(path):
    return json.loads(Path(path).read_text())


def build_row(row, snapshot_root, out_root):
    row_dir = out_root / row["row_id"]
    files_dir = row_dir / "files"
    outputs_dir = row_dir / "outputs"
    if row_dir.exists():
        shutil.rmtree(row_dir)
    files_dir.mkdir(parents=True)
    outputs_dir.mkdir(parents=True)

    repo_snapshot_dir = snapshot_root / repo_dir(row["source_repo"])
    missing = []
    copied_files = []
    for relpath in row["files"]:
        src = repo_snapshot_dir / relpath
        if not src.exists():
            missing.append(relpath)
            continue
        dest = files_dir / relpath
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied_files.append(relpath)

    pack = {
        "row_id": row["row_id"],
        "spec_display": row["spec_display"],
        "source_kind": row["source_kind"],
        "source_repo": row["source_repo"],
        "source_commit": None,
        "source_commit_pinned": False,
        "comparison_unit": row["comparison_unit"],
        "entrypoint_files": row["entrypoint_files"],
        "allowed_files": copied_files,
        "missing_files": missing,
        "surface_taxonomy": [
            "entry_brief",
            "rules_workflow",
            "implementation_code",
            "tests_checks",
            "evidence_records",
            "specs_plans",
            "qa_release_review"
        ]
    }
    (row_dir / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n")
    return {
        "row_id": row["row_id"],
        "pack_dir": str(row_dir),
        "copied_file_count": len(copied_files),
        "missing_file_count": len(missing),
        "missing_files": missing,
    }


def main():
    args = parse_args()
    config = load_config(Path(args.config))
    snapshot_root = Path(args.snapshot_root).resolve()
    out_root = Path(args.out_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    rows = config["rows"]
    if args.row_id:
        rows = [row for row in rows if row["row_id"] == args.row_id]
        if not rows:
            raise SystemExit(f"row_id {args.row_id!r} not found in config")

    results = [build_row(row, snapshot_root, out_root) for row in rows]
    print(json.dumps({"built": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
