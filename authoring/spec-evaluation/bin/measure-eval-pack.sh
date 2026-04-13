#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

exec uvx --from tiktoken python "$script_dir/../scripts/measure_eval_pack.py" "$@"
