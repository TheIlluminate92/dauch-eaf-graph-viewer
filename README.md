# Dauch EAF Graph Viewer

A Windows graph viewer for reviewing electric arc furnace (EAF) recordings. Drop in supported **RPH** files, choose the signals you want to see, and compare how they change through a heat or plot one recorded variable against another.

Built for Sergio's SmartArc review workflow: set up a useful signal view once, save it, and reuse it across recordings. The viewer opens in your browser, but the files and processing stay on your computer. The packaged app works offline and does not require Python to be installed.

**[Download the Windows app](https://github.com/TheIlluminate92/dauch-eaf-graph-viewer/releases/latest)** · **[Detailed how-to](docs/USER_GUIDE.md)** · **[Troubleshooting](docs/OPERATIONS.md)**

## What this does

The viewer turns recorded signal data into charts you can inspect, zoom into and compare. Use it to look at phase-current differences, changes in power, stability factors, impedance response and electrode movement. Keep several readings visible with pinned crosshairs, or put multiple heats on the same chart to compare their patterns.

It provides the recorded evidence for your review. It does not diagnose faults automatically, assign alarm thresholds or calculate controller tuning changes. Signal meanings, units and scaling still need the site's documentation.

## Download and run

1. Download `Dauch_EAF_Graph_Viewer_Windows.zip` from [Releases](https://github.com/TheIlluminate92/dauch-eaf-graph-viewer/releases/latest).
2. **Extract the entire ZIP**, then open `Dauch EAF Graph Viewer.exe`.
3. Keep its `engine` folder beside the EXE and keep the launcher open while using the browser.
4. Drop your RPH files into the launcher or webpage, or choose **Add RPH files**.

Download access follows the repository's visibility. The extracted app itself runs locally without GitHub.

The Windows ZIP includes a local **README.md**, a detailed **PROGRAM-GUIDE.md**, and **Open Guides in VS Code.cmd**. Open the guides with that shortcut, then press **Ctrl+Shift+V** in VS Code for formatted preview. They explain how to use the program, including its controls, features and a complete first-comparison walkthrough.

## Your first review

1. **Load a recording.** Use the launcher or **Add RPH files** on the page. Check the filename shown above the chart.
2. **Choose a starting view.** The five standard views group related signals; see the table below.
3. **Inspect an interval.** Turn the mouse wheel to zoom, drag a rectangle to focus on a region, and double-click to reset.
4. **Keep a reading.** Click inside the chart to pin its time and axis coordinates. Move the mouse away and the reading stays visible.
5. **Compare heats.** Add more files and select **Overlay files**, or use **One file at a time** with Previous/Next.
6. **Save your setup.** Adjust signals, axes and colors, name the view, and click **Save**. Choose that saved view the next time you load recordings.

For a complete worked walkthrough, see [Sergio's first comparison](docs/USER_GUIDE.md#walkthrough-sergios-first-comparison).

## Five standard views

| View | Signals grouped together | Use it to inspect |
| --- | --- | --- |
| Power & heat progress | Total power and accumulated energy | How power and energy change through the recording. |
| Phase current balance | Three phase currents and current reference | Phase differences, divergence and dropouts. |
| Arc stability factors | SF1–3 and VoltSF1–3 | Changes in the recorded factors and differences between phases. |
| Impedance response | ZFeedback1–3 and Sp1Imped–Sp3Imped | Response timing and oscillation on separate recorded scales. |
| Electrode response | Electrode positions and regulator outputs | Motion alongside changes in regulator output. |

Every view is a starting point. Search **All signals** to add tags, then use **Y-L/Y-R** to select their vertical axis. The [operator guide](docs/USER_GUIDE.md#five-standard-views) lists the exact tags. Impedance feedback and setpoints use different recorded scales; numerical tracking error requires confirmed scaling.

## Choose X and Y variables

1. Search **All signals** for the horizontal variable, such as `MWTot`, and click its **X** button. The viewer switches to **Recorded signal (X–Y)** and initially selects **Scatter**.
2. Check the variables you want on Y, such as `Current1`. Use **Clear Y selection** first if you want a clean comparison. Choosing a new X removes that variable from Y; you may explicitly check it again to plot a variable against itself.
3. Under **Selected Y signals**, use **Y-L** for the left vertical scale or **Y-R** for the right. These are both Y axes. The **X signal** dropdown above the graph chooses the single horizontal variable.
4. Choose **Overlay files** to compare all checked heats, or **One file at a time** and Previous/Next to cycle through them.
5. Name and **Save** the view. It remembers the X variable, all Y variables, axes, colors and display settings. Export/Import includes the X selection too.

For example, X = `MWTot` and Y = `Current1` shows how phase current varies with total power. Each dot pairs X and Y from the **same sample in the same recording**. Files are never joined to one another. Hover over a dot for its X/Y values, original UTC timestamp and elapsed minutes.

Scatter is usually easiest to read for this comparison. If you choose Lines or Lines + points, samples connect in recording order: X is **not sorted**, so lines can double back. Recording gaps and missing values remain broken. A file without the chosen X signal is skipped with a visible message; it is never assigned a substitute variable.

Crosshairs and pins show the chosen X variable's value, plus the left/right Y coordinates. These cursor coordinates can fall between actual samples. Changing X clears old pins and zoom. To return to a time plot, choose **Minutes from file start** or **Recorded time (UTC)** under **X axis**, or select a standard view.

## Chart controls

| Action | Control |
| --- | --- |
| Zoom in or out | Mouse wheel over the chart. |
| Zoom into a region | Click and drag a rectangle. |
| Reset zoom | Double-click the plot. |
| Move a zoomed chart | Select Pan in the chart toolbar, then drag. |
| Read a recorded sample | Hover over a plotted trace or point for its tooltip. |
| Keep cursor coordinates | Click once inside the chart to add a numbered pin. |
| Select or remove a pin | Click its sidebar row, or its X. |
| Resume mouse tracking | Click **Live cursor**; existing pins remain in the list. |
| Remove all pins | Click **Clear pins**. |
| Change the display | Choose **Lines**, **Scatter** or **Lines + points**. |
| Make lines finer | Choose **Thickness**, from 0.5 to 3 pixels. |
| Save a chart image | Use the camera button in the toolbar. |

Up to **ten pins** can be kept at once. Pins capture the cursor's X (time or signal) and left/right Y coordinates; actual recorded samples are shown separately in trace tooltips. Pins remain readable after the pointer leaves and keep their numeric values through zoom and display-style changes.

Changing recordings, selected signals, axis assignments or the X axis clears pins. Pins are temporary and are not included in saved views or PNG exports.

## Compare recordings and reuse views

**Overlay files** draws the checked recordings together. **Minutes from file start** aligns their first samples at zero; it does not automatically align process events. Choose **Recorded time (UTC)** when absolute timestamps matter. **One file at a time** lets you cycle through recordings with the same signal selection.

Saved views remember signals, left/right axes, colors, comparison mode, X axis and X signal, line shape, thickness and plot style. Use **Export view** and **Import view** to move a configuration between PCs. Load the recording files again in each new session; saved views do not contain recording data, zoom ranges or pins.

Settings are stored at:

```text
%LOCALAPPDATA%\Dauch\EAF Graph Viewer\views.json
```

See [backup and recovery](docs/OPERATIONS.md#back-up-and-recover-saved-views) before replacing or restoring that file.

## Features at a glance

- All signals in the supported recording layout; the five supplied real recordings contain 644 signals each.
- Five starter views for power/heat progress, phase current balance, arc stability factors, impedance response, and electrode response.
- Individual recording navigation or overlaid comparisons; elapsed minutes or recorded UTC time.
- Any recorded variable on X, one or more on Y, with separate left/right Y scales, colors, saved views and JSON import/export.
- Lines, scatter, or both; straight/step lines and thickness from 0.5 to 3 pixels.
- Mouse-wheel zoom, drag-to-zoom, double-click reset, and PNG chart export.
- Live crosshair with X and both Y axis coordinates; click to keep up to ten numbered points.

## Documentation

Erik owns product decisions; Reporter Recreation owns implementation; Work Historian owns documentation organization. Start maintenance with [current handoff](docs/HANDOFF.md) and [worker instructions](AGENTS.md).

- [Operator guide](docs/USER_GUIDE.md): everyday workflow, presets, saved views, pins, and comparisons.
- [Architecture and RPH format](docs/ARCHITECTURE.md): components, data handling, format boundaries, and local service routes.
- [Development and release](docs/DEVELOPMENT.md): exact versions, build commands, tests, and packaging.
- [Troubleshooting and recovery](docs/OPERATIONS.md): startup, plotting, saved-view backup, and rollback.
- [Validation and bug hunt](docs/VALIDATION.md): completed tests, fixes, evidence scope, and remaining limits.
- [Project history and handoff](docs/HISTORY.md): original CSV workflow, transition to RPH, and continuation notes.
- [Saved-view reference](docs/SAVED-VIEWS.md): fields, defaults and recovery checks.
- [Historian review](docs/HISTORIAN-REVIEW-2026-11-13.md): standards coverage and remaining acceptance.
- [Third-party components](docs/THIRD_PARTY.md).
- [Release changes](CHANGELOG.md).

## Data and scope

RPH is a binary recording format, not a renamed CSV. This reader supports the layout observed in the supplied recordings; other RPH variants remain unverified. Source recordings are not modified. Raw signal values are preserved, and gaps over five seconds break lines.

Real recordings, plant-derived test variants, and the earlier CSV reports are excluded from this repository and release assets. The source tests include small recordings generated from scratch. Private real-file checks are optional and are explicitly reported as skipped when fixtures are absent.

The current graph viewer does not open CSV files. The earlier notebook and CSV reporting program remain a separate predecessor workflow, described in the history document.

## Validation

The release was checked with five real RPH recordings, automated source tests, browser interaction checks and the actual packaged Windows engine and launcher. The six-file launcher check used those five recordings plus one derived test variant, through automated drop events. Downloaded release ZIPs matched their published SHA-256 checksums.

See the [validation record](docs/VALIDATION.md) for the bug fixes, exact test coverage and limits. Compatibility with other RPH layouts and a broad Windows/browser matrix has not been established.


## License and redistribution

[MIT License](LICENSE): reuse and modification are allowed with the notice retained. Provided as is, without warranty. See [licensing and packaging scope](LICENSING.md) for third-party terms and release limitations.
