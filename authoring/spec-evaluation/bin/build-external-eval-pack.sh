#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

exec python "$script_dir/../scripts/build_external_eval_pack.py" "$@"
