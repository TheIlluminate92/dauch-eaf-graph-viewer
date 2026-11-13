# Validation and bug hunt — 2026-11-13

## v1.0.0 release evidence

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

## v1.0.1 local program guides — 2026-11-13

This is a documentation/package update. Every original v1.0.0 ZIP entry, including the engine, launcher, frontend and dependency files, was compared byte-for-byte with the new ZIP and matched. The additions are local `README.md`, `PROGRAM-GUIDE.md` and `Open Guides in VS Code.cmd`. The v1.0.0 release assets remain unchanged.

The guides cover the program itself: startup, features, standard views, axes, controls, pins, saved views, file comparisons, a complete Sergio walkthrough, troubleshooting and recovery. All relative guide links and heading anchors were checked in the fresh extraction. The opener ran successfully with installed VS Code; an isolated environment without VS Code displayed the documented fallback instructions and made no installation/settings changes. VS Code preview formatting is standard Markdown; this package check did not include a new visual preview acceptance test.

The freshly extracted engine started successfully and served the viewer page, cursor script and session state. This was a startup/asset smoke check, not a repeat of the full v1.0.0 browser or recording test matrix. No new clean-machine, restore, signing or broad compatibility acceptance is claimed.

Windows ZIP SHA-256:

```text
60f7b8f70076b6659a9bad0fb360ff0d4773d2153772ad5063f8e583a8162945
```

The release checksum manifest covers both Windows and source archives. The source package includes the complete documentation and packaging changes. Neither archive includes private recordings.


## v1.1.0 X–Y plots — 2026-11-13

This runtime release adds true signal-versus-signal plotting. It was rebuilt in a clean virtual environment using the pinned dependencies and Python 3.12.14. The smaller archive reflects the clean build environment; it is not a reuse of the previous runtime ZIP.

| Check | Result and scope |
| --- | --- |
| Source regression | All 11 Python methods passed, including both private-real-recording checks (no skips). Node coordinate/pin regressions and inline JavaScript syntax passed. |
| Pairing correctness | Generated-from-scratch recordings verified same-row X/Y pairs, repeated/decreasing X, gap insertion, timestamps, left/right Y, identity X=Y, missing X, NaN/infinity handling and isolation across recordings. Old time views and invalid X settings were checked. |
| Fresh extracted engine | Passed against one real RPH plus five derived variants: all 644 columns individually on Y and as X; 30 individual preset plots; five preset overlays; six-file X–Y in Lines, Scatter and Both; line widths; saved time/X–Y views after restart; malformed-file rejection; offline assets. |
| Actual Windows launcher | Automated WinForms drop harness loaded five real files plus one distinct derived variant and re-enabled file selection. This is event injection, not physical mouse dragging. |
| Browser with packaged engine | Five real recordings: X/Y selection, right-only Y, overlays and filtering, individual cycling, UTC/time switching, same-sample tooltip timestamps, ten-pin cap, wheel zoom and double-click reset, unchanged pinned values after zoom, context clearing, saved-view restore/reload and exported X/Y JSON. |
| Error recovery | Missing X remained selected and was reported per file. Five-million-point rejection hid the old graph and cleared pins. Selecting a valid saved view recovered. No JavaScript warnings/errors were observed during the final valid-view checks. |
| Layout/races | Rapid Lines/Scatter/Both changes and a 1366 × 768 viewport check passed. Long Y descriptions are capped; Plotly's redundant responsive handler is disabled in favor of the existing serialized resize queue. The 1912 × 948 view had no document overflow. |
| Archive/guides | Shipped frontend bytes matched the browser-tested source. Local Markdown links/anchors passed. No RPH/CSV recordings or drop harness are included. The local README, walkthrough and START HERE explain X/Y selection and rollback limitations. |
| Notices | Project MIT notice, matching Python notice and available distribution notices were included. The collector reported no distributions with zero notice files in the clean environment; this is not a complete legal or vendored-component audit. |

Browser testing was against the newly built packaged engine; the fresh extracted ZIP engine was separately exercised by the automated suite. The exported configuration JSON was inspected after the browser download completed. A new native Import file-picker round trip was not performed; X–Y save/validation/restart is covered by source and packaged tests. Historical v1.0.0 interaction evidence above remains dated evidence, not a claim every earlier browser action was repeated.

The original five RPH files remained local and unchanged. No clean-machine or broader browser/Windows qualification, physical drag acceptance, signing or Sergio end-user acceptance is claimed. Pins remain temporary cursor coordinates, not sampled readings. v1.0.x cannot read new X–Y views; preserve pre-upgrade settings for rollback.

Windows v1.1.0 ZIP SHA-256:

```text
aa813c5466a54981945a6b5d312567dad0294b990f0fefebeec8833f3b97da6f
```

The source archive and release manifest bind this dated source/documentation snapshot. The final packaging pass refreshed only local documentation/notices; runtime entries were byte-compared with the tested extraction.
