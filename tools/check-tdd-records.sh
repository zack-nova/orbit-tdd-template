#!/usr/bin/env sh
set -eu

records_dir="${1:-docs/tdd/records}"

if [ ! -d "$records_dir" ]; then
  printf 'not_ready records_dir=%s reason=missing_records_dir\n' "$records_dir"
  exit 1
fi

count=0
bad=0

for record in "$records_dir"/*.md; do
  [ -e "$record" ] || continue
  [ "$(basename "$record")" = "README.md" ] && continue

  count=$((count + 1))

  for marker in \
    "Status:" \
    "Objective:" \
    "Files touched:" \
    "RED command:" \
    "RED result:" \
    "GREEN command:" \
    "GREEN result:" \
    "Final validation command:" \
    "Final validation result:"
  do
    if ! grep -Fq "$marker" "$record"; then
      printf 'not_ready record=%s missing=%s\n' "$record" "$marker"
      bad=1
    fi
  done

  if ! grep -Eq '^Status: (success|failure|blocked|abnormal_exit|external_stop)$' "$record"; then
    printf 'not_ready record=%s reason=invalid_status\n' "$record"
    bad=1
  fi
done

if [ "$count" -eq 0 ]; then
  printf 'not_ready records=0 reason=no_tdd_records\n'
  exit 1
fi

if [ "$bad" -ne 0 ]; then
  exit 1
fi

printf 'ready records=%s\n' "$count"
