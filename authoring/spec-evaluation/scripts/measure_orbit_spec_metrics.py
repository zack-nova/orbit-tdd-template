#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import tiktoken
except ImportError as exc:
    raise SystemExit(
        "tiktoken is required. Run via: uvx --from tiktoken python "
        "authoring/scripts/measure_readme_spec_metrics.py ..."
    ) from exc


def run(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def run_json(cmd, cwd=None):
    return json.loads(run(cmd, cwd=cwd))


def run_quiet(cmd, cwd=None):
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout


def format_k(tokens):
    return f"{round(tokens / 1000.0, 1):.1f}k"


def write_boundary_label(ratio):
    if ratio <= 0.30:
        return "narrow", "窄"
    if ratio <= 0.60:
        return "medium", "中"
    return "wide", "宽"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Measure scriptable README comparison metrics for one OrbitSpec."
    )
    parser.add_argument("--orbit", required=True, help="Orbit id to measure")
    parser.add_argument(
        "--publish-branch",
        help="Published branch to inspect. Defaults to orbit-template/<orbit>.",
    )
    parser.add_argument(
        "--tokenizer",
        default="o200k_base",
        help="tiktoken encoding name. Default: o200k_base",
    )
    parser.add_argument(
        "--skip-publish",
        action="store_true",
        help="Do not run `orbit template publish` before measuring.",
    )
    parser.add_argument(
        "--workdir",
        default=".",
        help="Repository root. Default: current directory.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(args.workdir).resolve()
    publish_branch = args.publish_branch or f"orbit-template/{args.orbit}"

    validate = run_json(["orbit", "validate", "--json"], cwd=repo_root)
    matching_orbits = [item for item in validate["orbits"] if item["id"] == args.orbit]
    if not matching_orbits:
        raise SystemExit(f"orbit {args.orbit!r} not found in orbit validate output")
    validate_orbit = matching_orbits[0]

    orbit_show = run_json(["orbit", "show", args.orbit, "--json"], cwd=repo_root)
    orbit = orbit_show["orbit"]
    if orbit.get("schema") != "members":
        raise SystemExit(
            f"orbit {args.orbit!r} does not use the member schema; current script expects member-schema output"
        )

    members = orbit["members"]
    surface_count = len(members)
    writable_surface_count = sum(
        1 for member in members if member["effective_scopes"]["write"]
    )
    ratio = 0.0 if surface_count == 0 else writable_surface_count / surface_count
    boundary_key, boundary_cn = write_boundary_label(ratio)

    publish_output = None
    if not args.skip_publish:
        publish_output = run_json(
            ["orbit", "template", "publish", "--orbit", args.orbit, "--json"],
            cwd=repo_root,
        )
        publish_branch = publish_output["branch"]

    encoder = tiktoken.get_encoding(args.tokenizer)
    tempdir = Path(tempfile.mkdtemp(prefix=f"readme-metrics-{args.orbit}-"))
    try:
        run_quiet(
            ["git", "worktree", "add", "--detach", str(tempdir), publish_branch],
            cwd=repo_root,
        )
        files_payload = run_json(["orbit", "files", args.orbit, "--json"], cwd=tempdir)
        files = files_payload["files"]

        token_rows = []
        total_tokens = 0
        max_path = None
        max_tokens = -1
        for relpath in files:
            content = (tempdir / relpath).read_text()
            tokens = len(encoder.encode(content))
            token_rows.append({"path": relpath, "tokens": tokens})
            total_tokens += tokens
            if tokens > max_tokens:
                max_tokens = tokens
                max_path = relpath

        result = {
            "repo_root": str(repo_root),
            "orbit_id": args.orbit,
            "publish_branch": publish_branch,
            "published": publish_output,
            "tokenizer": args.tokenizer,
            "static_files": files,
            "static_file_count": len(files),
            "static_file_tokens": token_rows,
            "static_load_tokens": total_tokens,
            "static_load_display": format_k(total_tokens),
            "max_file": {
                "path": max_path,
                "tokens": max_tokens,
                "display": format_k(max_tokens),
            },
            "surface_mode": "members",
            "surface_count": surface_count,
            "scope_count_from_validate": validate_orbit["scope_count"],
            "scope_count_matches_members": validate_orbit["scope_count"] == surface_count,
            "writable_surface_count": writable_surface_count,
            "write_boundary_ratio": ratio,
            "write_boundary_label": boundary_key,
            "write_boundary_display": f"{boundary_cn} ({writable_surface_count}/{surface_count})",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        try:
            run_quiet(
                ["git", "worktree", "remove", str(tempdir), "--force"],
                cwd=repo_root,
            )
        finally:
            shutil.rmtree(tempdir, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.output)
        raise
