# Dauch EAF Graph Viewer

A Windows graph viewer for inspecting EAF recordings and comparing heats. Drop one or more supported **RPH** files into the launcher, choose a signal view, and review the charts in your browser. Everything runs on the same computer; no Python installation or internet connection is needed for the packaged app.

Built for Sergio's SmartArc review workflow: choose the signals once, save the view, and reuse it across recordings. This is a visual inspection tool, not an automatic fault detector or controller tuning program.

## Download and run

1. Download `Dauch_EAF_Graph_Viewer_Windows.zip` from [Releases](https://github.com/TheIlluminate92/dauch-eaf-graph-viewer/releases/latest).
2. **Extract the entire ZIP**, then open `Dauch EAF Graph Viewer.exe`.
3. Keep its `engine` folder beside the EXE and keep the launcher open while using the browser.
4. Drop your RPH files into the launcher or webpage, or choose **Add RPH files**.

The repository and releases are private. A GitHub account with access is required to download; the extracted app itself runs locally without GitHub.

## Features

- All signals in the supported recording layout; the five supplied real recordings contain 644 signals each.
- Five starter views for power/heat progress, phase current balance, arc stability factors, impedance response, and electrode response.
- Individual recording navigation or overlaid comparisons; elapsed minutes or recorded UTC time.
- Custom left/right axes, colors, saved views, and JSON view import/export.
- Lines, scatter, or both; straight/step lines and thickness from 0.5 to 3 pixels.
- Mouse-wheel zoom, drag-to-zoom, double-click reset, and PNG chart export.
- Live crosshair with time and both axis coordinates; click to keep up to ten numbered points.

Pins remain readable after moving the mouse away. They survive zoom and display-style changes, but clear when the recordings, selected signals, axis assignments, or time axis change. Pins are temporary and do not appear in the PNG export. They capture **cursor coordinates**, not a sampled value for every signal.

## Documentation

- [Operator guide](docs/USER_GUIDE.md): everyday workflow, presets, saved views, pins, and comparisons.
- [Architecture and RPH format](docs/ARCHITECTURE.md): components, data handling, format boundaries, and local service routes.
- [Development and release](docs/DEVELOPMENT.md): exact versions, build commands, tests, and packaging.
- [Troubleshooting and recovery](docs/OPERATIONS.md): startup, plotting, saved-view backup, and rollback.
- [Validation and bug hunt](docs/VALIDATION.md): completed tests, fixes, evidence scope, and remaining limits.
- [Project history and handoff](docs/HISTORY.md): original CSV workflow, transition to RPH, and continuation notes.
- [Third-party components](docs/THIRD_PARTY.md).
- [Release changes](CHANGELOG.md).

## Data and scope

RPH is a binary recording format, not a renamed CSV. This reader supports the layout observed in the supplied recordings; other RPH variants remain unverified. Source recordings are not modified. Raw signal values are preserved, and gaps over five seconds break lines.

Real recordings, plant-derived test variants, and the earlier CSV reports are excluded from this repository and release assets. The source tests include small recordings generated from scratch. Private real-file checks are optional and are explicitly reported as skipped when fixtures are absent.

The current graph viewer does not open CSV files. The earlier notebook and CSV reporting program remain a separate predecessor workflow, described in the history document.
