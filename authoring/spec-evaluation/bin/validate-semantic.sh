#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

exec python "$script_dir/../scripts/validate_semantic_eval.py" "$@"
