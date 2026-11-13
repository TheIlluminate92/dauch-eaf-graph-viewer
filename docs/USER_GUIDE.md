# Operator guide

## Open and compare recordings

Extract the Windows ZIP completely. Open the launcher and add one or several `.rph` files. The browser address begins with `127.0.0.1`, which is this computer. Keep the launcher open; closing it stops its viewer service.

Choose **One file at a time** to use Previous/Next or the recording dropdown. Choose **Overlay files** to draw included recordings together. The file checkboxes control inclusion in overlays; the X removes a recording from the session. Duplicate contents load only once, even under another filename.

**Minutes from file start** aligns each file's first sample at zero. This is not automatic alignment to power-on, a process event, or an equivalent heat stage. **Recorded time (UTC)** compares absolute timestamps. Gaps longer than five seconds remain blank rather than being connected.

## Five standard views

| View | Left axis | Right axis | Purpose |
| --- | --- | --- | --- |
| Power & heat progress | MWTot | MWH_PX3 | Review power and accumulated energy through the heat. |
| Phase current balance | Current1, Current2, Current3, CurrentRef | None | Compare phases, divergence, and dropouts. |
| Arc stability factors | SF1, SF2, SF3 | VoltSF1, VoltSF2, VoltSF3 | Compare changes and phase differences. |
| Impedance response | ZFeedback1, ZFeedback2, ZFeedback3 | Sp1Imped, Sp2Imped, Sp3Imped | Compare response timing and oscillation on separate scales. |
| Electrode response | EPos1_PX3, EPos2_PX3, EPos3_PX3 | RegOut1, RegOut2, RegOut3 | Inspect electrode motion and regulator-output changes. |

These groupings use the actual recorded tags. Factor meanings, engineering units, scaling, and good/bad limits require site/vendor documentation. In particular, impedance feedback and setpoints have different recorded scales: do not subtract the displayed numbers as if they were confirmed matching units.

## Customize and save a view

Search **All signals**, check the desired tags, and set each selected Y signal to Y-L or Y-R. Use the color picker to distinguish signals. A view remembers signals, axis assignments, colors, comparison mode, X axis (time or a recorded signal), line shape, thickness, and plot style.

Give the view a name and click **Save**. Choose it under **My saved views** next time. Export/Import view shares a JSON configuration with another PC. Saved views do not bind to particular recording files, zoom ranges, or pinned points.

Saved settings live in `%LOCALAPPDATA%\Dauch\EAF Graph Viewer\views.json`. Recordings must be reopened in each new launcher session.

## Plot one variable against another (X–Y)

1. Search **All signals** for the horizontal variable, such as `MWTot`, and click its **X** button. The viewer switches to **Recorded signal (X–Y)** and initially selects **Scatter**.
2. Check the variables you want on Y, such as `Current1`. Use **Clear Y selection** first if you want a clean comparison. Choosing a new X removes that variable from Y; you may explicitly check it again to plot a variable against itself.
3. Under **Selected Y signals**, use **Y-L** for the left vertical scale or **Y-R** for the right. These are both Y axes. The **X signal** dropdown above the graph chooses the single horizontal variable.
4. Choose **Overlay files** to compare all checked heats, or **One file at a time** and Previous/Next to cycle through them.
5. Name and **Save** the view. It remembers the X variable, all Y variables, axes, colors and display settings. Export/Import includes the X selection too.

For example, X = `MWTot` and Y = `Current1` shows how phase current varies with total power. Each dot pairs X and Y from the **same sample in the same recording**. Files are never joined to one another. Hover over a dot for its X/Y values, original UTC timestamp and elapsed minutes.

Scatter is usually easiest to read for this comparison. If you choose Lines or Lines + points, samples connect in recording order: X is **not sorted**, so lines can double back. Recording gaps and missing values remain broken. A file without the chosen X signal is skipped with a visible message; it is never assigned a substitute variable.

Crosshairs and pins show the chosen X variable's value, plus the left/right Y coordinates. These cursor coordinates can fall between actual samples. Changing X clears old pins and zoom. To return to a time plot, choose **Minutes from file start** or **Recorded time (UTC)** under **X axis**, or select a standard view.

## Read and pin coordinates

Move the mouse inside the plotting area for a vertical X line and a horizontal coordinate line. Labels show time or the chosen X signal value along the bottom and the corresponding left/right axis coordinates. A missing axis displays a dash. Signal tooltips separately show actual recorded samples.

Click once to keep that crosshair in place. Each click adds a numbered pin, up to ten. The sidebar lists its original X value and Y coordinates, so the readings remain available even if zoom moves the point off-screen.

- Click a pin's row to select its crosshair.
- Click its X to remove that point and free a slot.
- **Live cursor** resumes mouse tracking while retaining the pin list.
- **Clear pins** removes all points.

Pins keep their numeric coordinates while zooming or changing line thickness, color, or plot style. Changing recordings, selected signals, left/right assignments, or the X axis clears the pins to avoid applying old coordinates to a different chart. Pins are temporary to this page session and are not saved in views or included in PNG exports.

A click is briefly delayed so double-click reset still works. A drag selects a zoom region rather than adding a pin.

## Chart controls

Use the mouse wheel over the chart to zoom, drag a region to zoom into it, and double-click to reset. The toolbar also offers pan, zoom, reset, and PNG export. Click legend entries to hide/show individual traces.

**Scatter** shows sample points. **Lines + points** shows both. Thickness and line-shape controls are inactive for scatter-only plots. File marker shapes and line dash patterns distinguish recordings; these repeat after six files.

The main page fits the browser window. Scroll inside the sidebar or pin list to reach longer content. Very small windows can reduce chart space; maximize the browser for detailed comparisons.

## Walkthrough: Sergio's first comparison

### 1. Get a single heat on screen

Open the extracted Windows launcher. Click **Add RPH files**, select a supported recording and wait for it to finish loading. In the browser choose **One file at a time** and **1 · Power & heat progress**. Confirm the filename and sample/duration caption above the chart match the recording you intended to open.

The left axis is MWTot; the right is MWH_PX3. Move the pointer over a plotted trace to see a recorded sample tooltip. Move elsewhere inside the chart to read the crosshair coordinates. These are different readings: the crosshair can sit between samples or above/below a trace.

### 2. Examine a smaller interval

Place the pointer over the time interval of interest and turn the mouse wheel to zoom. For a specific rectangle, press and drag across that region. Double-click the plot to reset if you lose your place. The toolbar's pan option lets you move a zoomed view without creating another zoom rectangle.

### 3. Keep readings visible

Click at one position of interest. After the short click delay, P1 appears and its row shows time, left and right coordinates. Move the pointer into the sidebar: the selected crosshair and values stay visible.

Click a second position for P2. Select the P1 row to inspect it again. Add more points as needed, up to ten; remove one with its X before adding an eleventh. Use **Live cursor** to track the mouse while retaining existing pins. Use **Clear pins** when finished with those points.

If zoom hides a pinned point, its table readings remain unchanged and the readout identifies it as outside the current zoom. Reset zoom to see it again. Write down or screenshot important pin readings before changing the recording or signal axes.

### 4. Compare another heat

Add a second recording, then choose **Overlay files**. Both checked files share the plot. With **Minutes from file start**, zero means each file's first recorded sample; it does not guarantee that process stages line up. Use the legend and dash patterns to identify each recording. Uncheck a file to temporarily exclude it from the overlay.

Switch back to **One file at a time** and use **Next**/**Previous** to inspect the same selected signals on each heat. Pins clear when the plotted recording set changes. If actual clock timing matters, choose **Recorded time (UTC)** instead of elapsed minutes.

### 5. Make a view he can reuse

Start from **2 · Phase current balance**. Search for a tag using the signal search field and check it to add it. Under **Selected Y signals**, choose Y-L/Y-R and a color for each tag. Remove unwanted tags with their X. Choose the desired plot style and thickness.

Enter a descriptive name such as `Sergio - phase current review` and click **Save**. Select another standard view, then choose the saved name under **My saved views** to restore that setup. If you reuse an existing name, confirm replacement only when you mean to update that view.

Use **Export view** to save the configuration JSON. On another PC, open the viewer, load appropriate recordings, click **Import view**, and select that JSON. The imported view is saved locally. Missing tags are reported rather than substituted.

### 6. Finish and reopen later

Use the chart camera button for a PNG of the plotted data. It does not include the pin overlay or pin table. Keep a screenshot separately if the temporary readings must be retained.

Close the launcher when finished. Next time, reopen the app, add the recordings, and select the saved view. Signal/display settings return; the previous recordings, zoom range and pins do not.
