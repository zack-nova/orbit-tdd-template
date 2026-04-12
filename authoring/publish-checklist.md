# Publish Checklist

Use this checklist before publishing the `tdd` orbit from source to template.

1. Confirm `.harness/manifest.yaml` declares `kind: source`.
2. Confirm `.harness/manifest.yaml` locks `source.orbit_id` to `tdd`.
3. Review `.harness/orbits/tdd.yaml` as the authored truth.
4. If root `AGENTS.md` changed, run `orbit brief backfill --orbit tdd`.
5. Confirm source-only files are not in the export surface:
   - `authoring/**`
   - `references/**`
   - `tdd_related_repos_notes.md`
   - root `AGENTS.md`
6. Check exported rules and process docs for RED/GREEN/REFACTOR consistency.
7. Run the cheap record probe only when runtime records exist:
   `tools/check-tdd-records.sh`.
8. Run `orbit template publish --orbit tdd` and inspect the published payload.
