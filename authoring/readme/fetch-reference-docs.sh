#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(CDPATH= cd -- "$script_dir/../.." && pwd)"
out_dir="${1:-$repo_root/references/repo-docs-latest}"

fetch_with_gh() {
  local repo="$1"
  local path="$2"
  gh api -H "Accept: application/vnd.github.raw" "repos/$repo/contents/$path"
}

fetch_with_curl() {
  local repo="$1"
  local path="$2"
  local branch
  for branch in main master; do
    if curl -fsSL "https://raw.githubusercontent.com/$repo/$branch/$path"; then
      return 0
    fi
  done
  return 1
}

fetch_file() {
  local repo="$1"
  local path="$2"
  local repo_dir="${repo//\//__}"
  local dest="$out_dir/$repo_dir/$path"
  local tmp

  mkdir -p "$(dirname -- "$dest")"
  tmp="$(mktemp)"
  echo "fetch $repo:$path"
  for attempt in 1 2 3; do
    if command -v gh >/dev/null 2>&1; then
      if fetch_with_gh "$repo" "$path" >"$tmp"; then
        mv "$tmp" "$dest"
        return
      fi
    elif command -v curl >/dev/null 2>&1; then
      if fetch_with_curl "$repo" "$path" >"$tmp"; then
        mv "$tmp" "$dest"
        return
      fi
    else
      rm -f "$tmp"
      echo "error: either GitHub CLI 'gh' or 'curl' is required" >&2
      exit 1
    fi
    if [[ "$attempt" == 3 ]]; then
      rm -f "$tmp"
      echo "error: failed to fetch $repo:$path" >&2
      exit 1
    fi
    sleep "$attempt"
  done
}

rm -rf "$out_dir"
mkdir -p "$out_dir"

fetch_file "garrytan/gstack" "README.md"
fetch_file "garrytan/gstack" "qa/SKILL.md"
fetch_file "garrytan/gstack" "ship/SKILL.md"

fetch_file "gsd-build/get-shit-done" "README.md"
fetch_file "gsd-build/get-shit-done" "get-shit-done/workflows/add-tests.md"
fetch_file "gsd-build/get-shit-done" "get-shit-done/workflows/verify-work.md"
fetch_file "gsd-build/get-shit-done" "get-shit-done/workflows/verify-phase.md"
fetch_file "gsd-build/get-shit-done" "get-shit-done/references/verification-patterns.md"

fetch_file "bmad-code-org/BMAD-METHOD" "docs/reference/testing.md"
fetch_file "bmad-code-org/BMAD-METHOD" "docs/reference/modules.md"

fetch_file "Fission-AI/OpenSpec" "README.md"
fetch_file "Fission-AI/OpenSpec" "docs/concepts.md"
fetch_file "Fission-AI/OpenSpec" "docs/workflows.md"
fetch_file "Fission-AI/OpenSpec" "docs/commands.md"
fetch_file "Fission-AI/OpenSpec" "docs/getting-started.md"

fetch_file "Yeachan-Heo/oh-my-claudecode" "AGENTS.md"
fetch_file "Yeachan-Heo/oh-my-claudecode" "docs/REFERENCE.md"

fetch_file "affaan-m/everything-claude-code" "README.md"
fetch_file "affaan-m/everything-claude-code" "agents/tdd-guide.md"
fetch_file "affaan-m/everything-claude-code" "skills/tdd-workflow/SKILL.md"
fetch_file "affaan-m/everything-claude-code" "commands/tdd.md"
fetch_file "affaan-m/everything-claude-code" ".opencode/prompts/agents/tdd-guide.txt"
fetch_file "affaan-m/everything-claude-code" ".kiro/agents/tdd-guide.md"

fetch_file "github/spec-kit" "README.md"
fetch_file "github/spec-kit" "spec-driven.md"
fetch_file "github/spec-kit" "templates/commands/implement.md"
fetch_file "github/spec-kit" "templates/commands/tasks.md"
fetch_file "github/spec-kit" "templates/commands/constitution.md"
fetch_file "github/spec-kit" "docs/quickstart.md"

fetch_file "obra/superpowers" "README.md"
fetch_file "obra/superpowers" "skills/test-driven-development/SKILL.md"

echo "updated reference snapshot: $out_dir"
