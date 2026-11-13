# Maintainer role and current handoff

Reviewed November 13, 2026 (America/Chicago). This is the concise continuation sheet; [README](../README.md) routes to the full technical guides.

## Current publication and licensing

As of November 13, 2026, GitHub reports this repository public, matching the owner's publication instruction. The owner subsequently authorized MIT for original project code. See [LICENSING](../LICENSING.md); the older private-publication checks below are historical, not the current visibility. v1.1.0 includes project/Python/distribution notices and the tested X–Y runtime; earlier release assets remain unchanged.

## Current implementation — v1.1.0

Sergio clarified that X must be a chosen recorded variable and Y another variable. v1.1.0 adds that workflow: the sidebar X button or X signal dropdown selects one horizontal tag; checkboxes select Y variables with Y-L/Y-R scales. Views persist the X tag, tooltips retain sample timestamps, and pins label the chosen variable. Pairing is within each file and sample, without sorting or interpolation.

Source checks, five-real-file browser checks, the fresh packaged engine (all 644 tags on each axis), and the native six-file drop harness passed. See the dated [v1.1.0 evidence](VALIDATION.md#v110-xy-plots--2026-11-13). Operator/local guides are updated. Historian retains organization ownership after the release handoff. Sergio end-user acceptance and the open items below remain outstanding.

Old time views load in v1.1.0. Older v1.0.x apps cannot read new X–Y views; preserve a pre-upgrade settings backup for rollback.

## Ownership and accepted baseline

Erik owns product scope and acceptance. Reporter Recreation owns implementation and packaging. Work Historian owns documentation and project-record organization following the completed publication handoff.

Originally private v1.0.0 was published at source commit `b121b18ecb78b2f718d2642738cc88cdb1c9a94f`. The annotated tag resolves to that commit. [Release](https://github.com/TheIlluminate92/dauch-eaf-graph-viewer/releases/tag/v1.0.0) includes Windows/source ZIPs and SHA256SUMS.txt. Current main may contain later documentation; those edits do not replace the v1.0.0 assets.

Historian independently checked repository privacy, source/tag identity, release metadata and remote operator documentation. Package redownloads, archive inspection and runtime tests remain the publisher's evidence in [VALIDATION](VALIDATION.md). No new runtime acceptance was performed by documentation review.

## Operate, build and recover

Use [the Sergio walkthrough](USER_GUIDE.md#walkthrough-sergios-first-comparison), [architecture](ARCHITECTURE.md), [build and test guide](DEVELOPMENT.md) and [troubleshooting/recovery](OPERATIONS.md). The settings contract is in [saved-view reference](SAVED-VIEWS.md). Read [worker instructions](../AGENTS.md) before edits.

## Open work and owners

| Gap | Owner and next evidence |
|---|---|
| Sergio's end-user acceptance | Erik/Sergio: confirm real workflow and report exact release, symptoms and expected behavior. |
| Clean-machine installation and broader Windows/browser support | Implementation owner: test a defined target and record exact environment. Current evidence covers the documented build machine. |
| Code signing | Erik and implementation owner: decide distribution needs; signing is not established. |
| Restore/rollback acceptance | Implementation owner: demonstrate view recovery and application rollback in isolated settings; current recovery instructions are procedures, not a completed restore receipt. |
| Additional RPH formats, units/scaling | Implementation owner with site/vendor evidence: validate formats and meanings before broadening claims. |
| Future release packaging | Implementation owner: preserve notices, review the explicit root documentation list and exclude private fixtures; bind tests/hashes to the new revision. |

Persisted annotations, pins in PNG exports and process-event heat alignment are proposals only. Preserve the existing session-only coordinate semantics until separately changed.

## Continue safely

Documentation/package update, November 13, 2026: v1.0.1 includes the expanded repository README and adds a local program README, full program walkthrough and VS Code guide opener to the Windows ZIP. This incorporates the historian's documentation baseline without removing its navigation. All original v1.0.0 archive files were byte-compared and are unchanged. Fresh extraction/startup, guide links and opener checks passed; see [validation](VALIDATION.md#v101-local-program-guides--2026-11-13). The prior full runtime test evidence remains v1.0.0 evidence. The Teams announcement is a draft for Erik to send. Erik stated he will make GitHub public for the recipient; the implementation owner does not change repository visibility as part of packaging.

Read current source and changed guides, identify the affected contract, and preserve evidence dates. Update current instructions and dated evidence in the same batch. No server, controller or plant change is authorized by this repository's documentation ownership.
