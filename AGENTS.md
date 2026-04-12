# Source Branch Agent Instructions

This repository is the Orbit source-branch authoring repo for the `tdd`
template.

## Source Of Truth

- `.harness/manifest.yaml` identifies this branch as `kind: source`.
- `.harness/orbits/tdd.yaml` is the authored OrbitSpec.
- `.harness/orbits/tdd.yaml` -> `meta.agents_template` is the installed-worker
  brief truth.
- `docs/tdd/**` and `tools/check-tdd-records.sh` are exported template content.
- `authoring/**`, `references/**`, this `AGENTS.md`, and `README.md` are
  source-only authoring material unless the OrbitSpec explicitly adds them to
  the export surface.

Do not add legacy `.orbit/config.yaml` or `.orbit/orbits/*.yaml` files. The
source branch should publish from the v0.4 hosted control plane.

## Updating Reference Inputs

1. Run `authoring/fetch-reference-docs.sh`.
2. Review the refreshed files under `references/repo-docs-latest/`.
3. Update the reference summary in `README.md` when the source set or takeaway
   changes.
4. Update `authoring/tdd-template-plan.md` when a design decision changes.
5. Only then update exported content in `.harness/orbits/tdd.yaml`,
   `docs/tdd/**`, or `tools/check-tdd-records.sh`.

The reference snapshot is ignored by Git. Treat it as local evidence for
authoring, not as publishable template content.

## Updating Template Content

- Prefer concise, original Orbit-specific guidance over copied reference text.
- Keep the worker contract centered on a valid RED, a minimal GREEN, and
  refactor only after GREEN.
- If you add a new exported file, update `.harness/orbits/tdd.yaml` so the
  correct member owns it and the export/orchestration scopes are explicit.
- If you change the installed-worker brief, edit
  `.harness/orbits/tdd.yaml -> meta.agents_template` directly.
- Do not run `orbit brief backfill` from this root `AGENTS.md`; this file is for
  source-branch maintainers, not the installed worker brief.

## Validation Flow

Run these before publishing:

```sh
sh -n tools/check-tdd-records.sh
orbit validate --json
orbit template publish --orbit tdd --json
git ls-tree -r --name-only orbit-template/tdd
```

The published payload should include the hosted manifest, the `tdd` OrbitSpec,
`docs/tdd/**`, and `tools/check-tdd-records.sh`. It should exclude
`authoring/**`, `references/**`, root `AGENTS.md`, and runtime TDD records other
than `docs/tdd/records/README.md`.
