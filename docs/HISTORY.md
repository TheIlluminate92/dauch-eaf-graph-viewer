# Project history and handoff

## Purpose and scope changes

The project began as a request to repair and explain a Python utility module and EAF analysis notebook using six supporting CSVs. It expanded into a Dauch-themed Windows drag-and-drop report program with readable results. That CSV reporting workflow is the predecessor, not this repository's runtime.

The next request changed the primary input to RPH recordings and clarified the product as a graph viewer for Sergio: all available signals, reusable views, multiple recordings, overlaid comparisons and independent cycling. The supplied RPH proved to be binary, rather than the CSV-like format initially expected.

Five starter views were then added for SmartArc review. Subsequent requests added finer/adjustable lines, crosshairs with both axes and time, a viewport-filling layout, mouse-wheel zoom, scatter plotting and finally up to ten locked points. The user explicitly requested a detailed bug hunt and testing of the packaged application before delivery.

On 2026-11-13 the user requested GitHub publication with all documentation and a check-in with the local historian. The repository is private; recording files and derived plant data are kept out of Git and release assets.

## Current handoff

The primary product is the Windows RPH viewer. The entry point is `EAFGraphViewer.cs`; its service is `graph_viewer.py`. See DEVELOPMENT for source/build/test instructions and VALIDATION for the completed evidence. Runtime data remains local, saved views use the per-user application directory, and pins are session-only overlays.

The original CSV notebook/report tools remain in the originating local workspace. They were regression-tested there but are not shipped as part of the graph viewer. Do not silently reintroduce CSV input or imply six real RPH fixtures: five real RPHs were supplied, while some six-file tests use derived variants.

The local Work Historian has been asked to inspect the source conversation and maintain the project index. Its records are separate from the code repository. Final repository/release receipts are supplied to that historian after publication.

## Future work must preserve

- Raw readings and recording gaps; no invented units, scale conversions or fault thresholds.
- The distinction between cursor coordinates and actual sample tooltips.
- Safe chart context changes, stable file styles, and serialized Plotly updates.
- Atomic saved-view persistence and preservation of damaged original settings.
- Runtime package validation in addition to source checks.
- Private fixture handling: modified real recordings remain sensitive source data.

Potential extensions such as persisted annotations, including pins in image exports, event-based heat alignment, and additional RPH formats are not implemented or promised by this release.
