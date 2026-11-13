# Architecture and format

## Components

| File | Responsibility |
| --- | --- |
| `EAFGraphViewer.cs` | WinForms launcher, file-drop/file-picker upload, browser opening, owned service lifetime. |
| `graph_viewer.py` | Local HTTP service, session recordings, trace construction, validation and saved views. |
| `rph_reader.py` | Validates and decodes the observed binary RPH layout. |
| `standard_views.py` | Five starter signal groupings and explanatory text. |
| `viewer.html` | Dauch interface, file/signal/view controls, serialized Plotly rendering. |
| `cursor_tools.js` | Axis coordinate math, pin store, click/drag distinction and overlays. |

The launcher starts the bundled engine without opening a console, reads its local URL, and opens the user's browser. The browser and launcher send file bytes to that engine. Decoded recordings remain in memory; only named view settings are persisted. Closing the launcher terminates the engine it created, not other viewer sessions.

The engine binds only to `127.0.0.1` on a dynamically assigned port. Every session uses a random URL path; requests require the expected Host and, if provided, Origin. Plotly and page assets are bundled locally. This is a single-computer application, not a network-hosted multi-user service. The URL is a local access secret, not a user authentication system.

## Observed RPH layout

All integer and float fields below are little-endian. This describes the layout implemented from the supplied files, not a vendor-wide format specification.

1. Fixed signature `81 07 0f 2c`; column count is an unsigned 16-bit value at byte offset 21.
2. Signal list starts at offset 23: one-byte name length followed by ASCII bytes for each column.
3. Unsigned 32-bit row count.
4. Each sample row: unsigned 16-bit column count followed by one 32-bit float per column.
5. Unsigned 16-bit timestamp count, which must equal the row count.
6. One 12-byte timestamp record per row: 32-bit seconds, 16-bit milliseconds, 16-bit bias field, 32-bit reserved field.
7. Four zero footer bytes.

The reader checks exact total length, count limits, row widths, ASCII names, unique names, milliseconds below 1000, zero reserved/footer values, and strictly increasing timestamps. The stored seconds plus milliseconds are treated as UTC; the bias field is not applied to shift the recorded instant. Unknown header bytes and the bias field are not otherwise interpreted.

Current implementation limits columns to 1–4096 and rows to 1–65535. Nonfinite signal samples become JSON nulls. No engineering-unit conversions, interpolation, smoothing, or sample reduction are performed. A null break is inserted at gaps greater than five seconds.

## Plot and pin state

Recordings are identified by a truncated SHA-256 content hash. Each receives a stable style index for its session. Trace IDs hash the recording ID plus signal name and start with a letter, so arbitrary tag punctuation cannot break Plotly selectors.

Each requested plot snapshots settings and uses a generation counter to reject stale responses. Plotly render and resize operations share a queue. During updates or failures, the old plot is hidden so it cannot appear to represent the new selection.

Pin identity is scoped to the recording IDs, signal/axis mapping and time-axis mode. Color, line width, chart style and zoom do not change that context. A pin stores immutable numeric time/left/right coordinates and is reprojected onto current axis ranges. Axis labels are projected independently when the two Y axes have been zoomed independently.

Single clicks are delayed 360 ms to distinguish double-click reset; movement over four pixels is treated as a drag. Mouse release is observed at the window because Plotly creates a temporary drag cover outside the plot. Pins and crosshairs are HTML overlays, separate from Plotly's PNG export.

## Saved views and limits

`views.json` is a list of validated view objects. Saves re-read it under an operating-system file lock and replace it atomically. Invalid existing settings are preserved and block saving until repaired or moved aside. Reading session state reloads the saved view file, allowing another window's completed saves to be discovered on refresh.

Uploads are limited to 128 MiB per file and 512 MiB total input bytes per session. A plot request is limited to five million samples across selected files/signals. This is a plotted-point limit, not a guarantee that every chart below it renders quickly. The guard is conservative when some requested signals are missing.

## Local routes

All routes are relative to the random session URL. They are implementation details, not a public compatibility contract.

| Method | Route | Purpose |
| --- | --- | --- |
| GET | root, `plotly.js`, `cursor_tools.js` | Bundled page assets. |
| GET | `state` | Recording metadata, starter views, saved views and warnings. |
| POST | `upload?name=...` | Raw RPH bytes. |
| POST | `plot` | JSON settings and recording IDs; returns traces and missing-tag notices. |
| POST | `save` | Validated named view JSON. |
| POST | `remove` | Remove a recording ID from memory. |
