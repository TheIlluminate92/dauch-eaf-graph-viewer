# Troubleshooting and recovery

## Startup and loading

| Symptom | Check/action |
| --- | --- |
| Launcher cannot find/start the engine | Extract the entire ZIP. Keep `engine` beside the launcher EXE. Do not run just the EXE from inside the ZIP. |
| Browser page no longer loads | Reopen the launcher and use **Open graph viewer**. Old local session URLs stop working when their launcher closes. |
| Recording rejected | Check it is a complete supported `.rph` file. CSV input and unknown binary layouts are not supported. Keep the original file for diagnosis. |
| A file appears only once | Identical contents are deduplicated, even with different filenames. |
| Upload stops partway through a group | Valid files already loaded remain available. Correct the failed file or load the remaining files separately. |
| Session is full | Remove recordings before adding more. Limits are 128 MiB per file and 512 MiB of input files per session. |
| Graph could not update / plot limit | Reduce files or selected signals. The five-million-point guard does not reduce raw data. The old chart stays hidden on failure. |
| Scatter controls are disabled | Line thickness and line shape apply to lines, not scatter-only points. |
| Missing X signal / no X–Y graph | Choose a recorded X signal and at least one Y signal. A recording lacking the selected X tag is skipped with a message. |
| Lines double back in X–Y | Lines follow sample time order; X is not sorted. Select Scatter to inspect individual pairs. |
| Pins disappeared | Check whether files, selected signals, axis assignments or X axis changed; these intentionally clear pins. Reloading the page also resets pins. |
| Pin is outside the current zoom | Its saved coordinates remain in the sidebar. Reset zoom or select a different pin. |
| Exported PNG has no pins | Pins/crosshairs are separate HTML overlays. Use the sidebar readings or a local screenshot if those must be retained. |
| Long controls are off-screen | Scroll inside the sidebar/pin list and maximize the window. The main page itself stays within the viewport. |

## Back up and recover saved views

1. Close all viewer launcher windows before making a settings backup or restoring an older file.
2. Copy `%LOCALAPPDATA%\Dauch\EAF Graph Viewer\views.json` to a dated backup. Individual JSON exports are also useful for sharing or restoring one view.
3. Keep original recording files separately; they are not embedded in the view settings.

If a saved-view warning appears, the app preserves the unreadable original and refuses to save over it. Copy it somewhere safe first. Then either repair the JSON using the [saved-view reference](SAVED-VIEWS.md), restore a known-good backup, or rename the damaged file and reopen the app for a fresh list. Do not discard the only copy.

Another open viewer can save views to the same folder. Saves are locked and atomic. The browser is not a live shared editor: refresh the page to discover another window's changes, which also resets temporary pins.

## Roll back the application

Close the launcher, back up `views.json`, and extract the earlier known-good ZIP into a separate folder. Launch that complete folder; do not mix an older EXE with a newer engine directory. The files are portable but saved views use the same per-user settings location unless source/engine `--views` is explicitly used.

Older versions may not understand newer view fields. Preserve the new settings backup and restore the corresponding older backup if necessary. v1.1.0 reads older time-based views, but v1.0.x cannot read X–Y views (`x: signal`). Restore the pre-upgrade settings copy when rolling back to v1.0.x; keep the newer copy separately.

## Diagnose a report

Record the app release/tag, Windows and browser versions, exact error text, selected signals/axes, comparison mode, and whether the problem happens with one file or only an overlay. Include a view JSON when appropriate; it contains configuration, not the recording samples. Keep RPH files and screenshots with real values in an approved private location.

The service does not maintain a persistent activity log. For startup diagnostics, a maintainer can run the bundled `engine\EAFGraphEngine.exe --no-browser --views <test-folder>` from a terminal. Keep its local session URL private while the process is running. Closing the terminal-launched engine is the maintainer's responsibility; the normal Windows launcher manages its own engine automatically.
