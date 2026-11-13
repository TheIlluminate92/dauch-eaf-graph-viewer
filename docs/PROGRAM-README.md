# Dauch EAF Graph Viewer

## Start here

This program displays recorded electric arc furnace signals so you can review a heat, compare recordings and save useful signal selections for next time. It opens in your browser, but the files and processing stay on this computer.

**[Open the full program walkthrough](PROGRAM-GUIDE.md)** for step-by-step instructions, exact signal names, controls and worked examples.

## Read these guides in VS Code

1. Double-click **Open Guides in VS Code.cmd** in this folder. It opens this README and the full program guide in VS Code.
2. Select the guide's tab, then press **Ctrl+Shift+V** for its formatted Markdown preview.
3. For text and preview side by side, press **Ctrl+K**, release the keys, then press **V**.
4. Use the linked headings below or the document outline to jump to a topic.

VS Code must already be installed to use that shortcut. No extra Markdown extension is required. The `.md` files can also be read as ordinary text. VS Code is only for reading the guides; it is not required to run the graph viewer.

## Open the program

1. Extract the entire downloaded ZIP to a folder.
2. Open **Dauch EAF Graph Viewer.exe**.
3. Keep the `engine` folder beside the EXE and keep the launcher window open.
4. Drop one or more supported `.rph` files onto the launcher, or click **Add RPH files**.
5. In the browser, choose a standard view to begin.

Python and an internet connection are not required for the packaged program. The Windows .NET Framework runtime and a browser are required. Closing the launcher stops its viewer session.

## What you can do

| Feature | How to use it |
| --- | --- |
| View available signals | Search **All signals**, check the tags you want, and assign each to the left or right axis. |
| Plot one variable against another | Click **X** beside the horizontal signal, then check the Y signals. See the [X–Y walkthrough](PROGRAM-GUIDE.md#plot-one-variable-against-another-xy). |
| Start with a useful grouping | Choose one of the five standard views listed below. |
| Compare heats | Choose **Overlay files** and include recordings with the file checkboxes. |
| Review heats individually | Choose **One file at a time**, then Previous/Next. |
| Save a setup | Name your signal/display configuration and click **Save**. |
| Share a setup | Use **Export view** and **Import view** for a configuration JSON. |
| Change the graph | Choose Lines, Scatter, or Lines + points; adjust thickness and line shape. |
| Inspect a smaller interval | Mouse wheel to zoom, drag a region, double-click to reset. |
| Keep readings visible | Click the chart to pin up to ten numbered coordinate readings. |
| Save an image | Use the camera button in the chart toolbar. |

## The five standard views

| View | Review focus |
| --- | --- |
| Power & heat progress | Total power and accumulated energy. |
| Phase current balance | Three phase currents and current reference. |
| Arc stability factors | SF1–3 and VoltSF1–3. |
| Impedance response | Feedback and setpoints on their separate recorded scales. |
| Electrode response | Electrode positions and regulator outputs. |

The [full guide](PROGRAM-GUIDE.md#five-standard-views) lists exact tags and explains the axes. These views help you inspect recorded behavior; they do not automatically diagnose faults or calculate tuning changes. Units, scaling and acceptable limits require site documentation.

## Pinning coordinates

Click once inside the plot. A numbered crosshair stays in place after you move the mouse away, and its sidebar row shows time or the chosen X variable, plus left/right Y coordinates.

- Add up to **10 points**.
- Click a row to select its crosshair; click its X to remove it.
- **Live cursor** resumes mouse tracking while keeping the points.
- **Clear pins** removes all of them.

Pins keep their values when you zoom or change line style. Changing recordings, signals, axis assignments or the X axis clears them. Pins are temporary and are not included in saved views or exported PNGs.

**Crosshair readings are cursor coordinates.** Hover tooltips on the traces show actual recorded sample values.

## What is remembered

Saved views retain the X variable or time mode, Y signals, colors, left/right assignments and display settings. Older time-based views still work. Back up settings before upgrading; v1.0.x cannot read new X–Y views. Reopen your RPH files each time; recording files, zoom and pins are not stored in a view.

Your saved views are stored at:

```text
%LOCALAPPDATA%\Dauch\EAF Graph Viewer\views.json
```

Keep a backup of that file or export important views. If the app reports damaged saved settings, preserve the original file before repairing or renaming it.

## Walkthrough and help

- [First comparison, step by step](PROGRAM-GUIDE.md#walkthrough-sergios-first-comparison)
- [Load and compare recordings](PROGRAM-GUIDE.md#open-and-compare-recordings)
- [Customize and save a view](PROGRAM-GUIDE.md#customize-and-save-a-view)
- [Choose variables for X and Y](PROGRAM-GUIDE.md#plot-one-variable-against-another-xy)
- [Read and pin coordinates](PROGRAM-GUIDE.md#read-and-pin-coordinates)
- [Chart controls](PROGRAM-GUIDE.md#chart-controls)
- [Troubleshooting and recovery](PROGRAM-GUIDE.md#troubleshooting-and-recovery)

## Recording limits

This viewer supports the observed binary RPH layout, including all 644 signals in the supplied recordings. It does not open CSVs. Unknown or incomplete formats are rejected. Original recordings are not modified; raw values are preserved and gaps over five seconds are shown as breaks.

Limits are 128 MiB per file, 512 MiB of input files per session and five million plotted samples per request. Reduce the selected signals or files if a comparison is too large. Elapsed-time overlays align the first samples at zero, not matching process events.
