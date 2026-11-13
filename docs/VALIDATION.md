# Validation and bug hunt — 2026-11-13

## Release evidence

The Windows runtime was tested as built, then zipped, freshly extracted and tested again. The shipped `viewer.html` and `cursor_tools.js` were byte-compared with the browser-tested sources. Runtime ZIP: approximately 51.1 MiB.

SHA-256 for `Dauch_EAF_Graph_Viewer_Windows.zip`:

```text
C2F74BBA88AADBA540181F0D439E042A26E2FABAD64EF43657E1A196692FC112
```

| Check | Result and scope |
| --- | --- |
| Full original workspace regression | 19 Python test methods passed: six analysis, five report and eight graph tests. CSV predecessor code is not part of this graph repository. |
| Graph source tests | All eight passed with the five private real RPHs. Repeated after portable fixture discovery was added. |
| Pin JavaScript tests | Passed: dual-axis/UTC/reversed-axis math, ten-point cap, immutable values, remove/reuse, context changes, single clicks, rapid separate clicks, drag, double-click, cancel and right-click handling. |
| Fresh extracted packaged engine | Passed: one real RPH plus five derived comparison variants, 30 individual preset plots, five overlays, all 644 signals individually, all six line widths, all three plot modes, saved-view restart, malformed-file rejection and offline asset loading. |
| Packaged Windows launcher | Passed: starts its engine, accepts an automated six-file drop event, loads exactly six distinct recordings, re-enables selection and closes its owned engine. Inputs: five real files plus one derived variant. This was event injection, not a physical mouse drag. |
| Browser, actual packaged engine | Passed: ten pins, rejection of an eleventh, remove/select/clear, Live cursor, persistence after pointer leaves, wheel/drag zoom, double-click reset, scatter and both modes, right-only axis, UTC timestamps, context clearing and file cycling/filtering. |
| Stale/error rendering | Plot-limit error hid the old chart and cleared pins; rapid style changes completed without final-run browser errors. Corrected trace IDs survived file filtering. |
| Layout | Final 1912 × 948 viewport had equal document/viewport dimensions, without page overflow. Sidebar remained independently scrollable. |

The real recordings were Hoeganaes23215 through 23219 (3,458; 3,486; 3,701; 3,117; 2,860 samples respectively), each with 644 signals. No recordings or screenshots with their values are distributed here. Derived variants remain plant data even when labelled synthetic.

## Bugs found and fixed

1. **Rapid plot/resize races:** overlapping renderer mutations could raise internal Plotly errors. Rendering and resize now share an ordered queue; stale responses are discarded.
2. **Wrong chart under new controls:** failed or pending updates could leave an older graph visible beneath a new heading. The chart is now hidden until the requested render succeeds.
3. **Filtering crash from trace IDs:** punctuation in a trace identifier was interpreted as a CSS selector. Stable trace IDs now use a letter-prefixed hexadecimal hash, with a regression check.
4. **Native timer binding:** the pin timer initially inherited an invalid browser invocation context. Timer calls now use explicit wrapper functions.
5. **Right-only coordinate capture:** crosshair geometry could depend on a missing left-axis layout. It now uses the populated axis geometry.
6. **Accidental or lost pins:** drag release may occur over Plotly's temporary cover, and rapid clicks can be confused with double-click reset. Window capture, movement thresholds and delayed click handling separate these cases.
7. **Pin drift after zoom:** original coordinates are immutable; each axis is projected independently, and off-screen points retain their table readings.
8. **Overlay count/style inconsistency:** file filtering now updates the counter, and remaining files retain their assigned line/marker styles.
9. **Zoom lost on cosmetic changes:** the persistence key now reflects semantic chart context, excluding color/width/style.
10. **Damaged view overwrite risk:** non-list JSON roots and invalid settings are rejected before use. Original settings are retained; saved views are reloaded safely across sessions.
11. **Misleading saved-view selection:** applying a preset clears an unrelated saved-view dropdown selection.
12. **Launcher startup cleanup:** failed startup clears the unusable URL, disables opening and terminates the owned failed engine. Local uploads explicitly bypass proxies and use bounded network timeouts.

## Limits of the evidence

This is a tested local Windows build, not a guarantee of zero defects. No clean-machine installer qualification, code-signing setup, long-duration endurance test or complete browser/Windows matrix was performed. Files with other RPH layouts are unverified. Rendering millions of points can be slow before the guard is reached.

Pins are cursor coordinates, not per-signal sampled values. They are temporary, are cleared on chart-context changes, and are absent from PNG export. Saved views do not persist recordings or zoom. The five preset groupings are project choices, not vendor-certified diagnostics. Units/scaling and alarm thresholds remain site-documentation questions.
