# References

The source branch keeps third-party reference snapshots local by default.

Use `authoring/fetch-reference-docs.sh` to refresh the comparison set into
`references/repo-docs-latest/`. The downloaded snapshot is intentionally ignored
by Git so the public template repository does not publish copied third-party
documentation as authored template source.

Keep the short comparison summary in root `README.md`.
