# Changes

## Unreleased — licensing maintenance (2026-11-13)

The project now has an MIT license. Future Windows/source ZIPs include it; Windows packaging also collects the matching Python license and available dependency notices. Existing v1.0.0/v1.0.1 releases remain immutable. See [LICENSING.md](LICENSING.md). No runtime behavior or existing release asset changed.

## v1.0.1 — 2026-11-13

- Bundled a program-specific local README and full walkthrough as Markdown, including controls, features, saved views, pins, comparison workflow and troubleshooting.
- Added an Open Guides in VS Code shortcut; VS Code remains optional for running the viewer.
- Expanded the repository README with the first-review workflow and chart-control reference.
- Packaging now includes current root instructions and local guides in the appropriate archives. Runtime application files are unchanged from v1.0.0.

### Historian documentation included

- Added current maintainer handoff, repository worker instructions, saved-view field reference and dated Historian standards review.
- Updated ownership/navigation and linked recovery instructions to the settings contract.
- Application code and v1.0.0 release assets are unchanged.

## v1.0.0 — 2026-11-13

First documented private GitHub release of the Windows RPH graph viewer.

- Windows file-drop launcher with a bundled local engine and Dauch browser interface.
- All recorded signals, five starter SmartArc views, editable/reusable views, multiple recording overlays and individual navigation.
- Lines/scatter/both, adjustable line thickness, elapsed/UTC axes and mouse-wheel zoom.
- Crosshair coordinates with up to ten pins, individual removal, clear-all and return-to-live controls.
- Fixed plot/resize races, stale graph display, unsafe trace identifiers, right-only-axis pinning, view validation and launcher failure cleanup.
- Added source, packaged-engine, native drop-event and browser validation evidence, plus operating, build, troubleshooting and recovery documentation.

Known scope: pins are temporary and excluded from PNG exports; CSV input belongs to the separate predecessor workflow; unsupported RPH layouts are rejected rather than guessed.
