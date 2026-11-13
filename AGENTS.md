# Repository work instructions

Start with [README](README.md) and [current maintainer handoff](docs/HANDOFF.md). Erik owns product decisions; Reporter Recreation owns implementation; Work Historian owns documentation organization. A handoff transfers context, not operational authority.

Keep this repository and releases private. Do not add recordings, CSV reports, plant-derived synthetic fixtures, screenshots with plant values, credentials, local session URLs or machine inventories. Generated-from-scratch test fixtures are distinct from modified real recordings.

Preserve raw values, gaps, format rejection, saved-view integrity and the difference between cursor coordinates and sampled values. Read the relevant architecture and validation sections before changes.

After meaningful work, update affected guides, HANDOFF and dated history/validation together. Distinguish source tests, packaged tests, browser checks and end-user acceptance. Do not claim a clean-machine test or restore based on source tests.

Inspect current branch, concurrent changes and deployment workflows before publishing. Keep release tags/assets immutable; release documentation is a dated snapshot. Future source packaging uses an explicit root-file list: check that new root documentation is included before promising it in a future source ZIP. Never force-push or overwrite another worker's edits.

Documentation-only edits need link/content/diff checks. Runtime changes need the relevant source tests and packaged/browser checks described in DEVELOPMENT and VALIDATION. Private fixture checks may explicitly skip; report those skips.

When giving Erik commands whose output should be pasted back, print a standalone `#####` line immediately before and after the relevant output.
