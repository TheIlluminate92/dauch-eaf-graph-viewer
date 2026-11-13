# Development and release

## Verified environment

The release was built and tested on x64 Windows, OS build `10.0.26300.0`, with Python `3.12.14`, Node `24.22.1`, and the installed .NET Framework compiler at `%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe` (file version `14.8.10001.0`). Browser interaction tests used Microsoft Edge on that machine. No clean Windows VM or broad Windows/browser compatibility matrix was completed.

Pinned Python dependencies are in `requirements-graph.txt`: NumPy `2.3.5`, Plotly `7.1.0`, PyInstaller `6.22.3`. Node is used only for the pin regression tests. The Windows runtime ZIP bundles Python and Python dependencies; users need the Windows .NET Framework runtime and a browser for the launcher/UI.

## Run from source

From the repository root in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-graph.txt
.\.venv\Scripts\python.exe graph_viewer.py
```

Optional engine arguments: recording paths as positional arguments, `--no-browser` to print the URL without opening it, and `--views <folder>` to isolate test settings. Never use the user's normal saved-view folder for destructive test fixtures.

## Automated source checks

```powershell
.\.venv\Scripts\python.exe -m unittest test_viewer -v
node test_cursor_tools.cjs
```

Six Python methods use recordings generated from scratch. Two more require the private real RPH fixtures and explicitly skip when unavailable. To run all eight, set `EAF_RPH_DIR` to the local folder containing `Hoeganaes23215.rph` through `Hoeganaes23219.rph`, then repeat the Python command. The default fixture folder is the current user's Downloads folder. Do not commit those recordings.

The tests validate parsing/corruption, gaps and overlays, HTTP boundaries, saved-view validation and persistence, external view changes, all presets against real tags, and stable file styles/trace IDs. The Node suite validates coordinate math, the ten-pin cap, immutability, ID reuse, context changes, clicks, drags, double-clicks and cancellation. It does not replace browser testing.

## Build and package

```powershell
.\build_graph_viewer.ps1
.\.venv\Scripts\python.exe package_graph_viewer.py
```

The build produces `release\graph-final\Dauch EAF Graph Viewer\`, containing the launcher and `engine` folder. The packager writes the Windows ZIP and source ZIP, checks ZIP integrity, and extracts the Windows ZIP into `outputs\graph-extracted-release\` for release testing. Build in a clean checkout for a release so old files cannot linger in output folders.

The published v1.0.0 Windows ZIP contains the exact application bytes tested in the browser and fresh-extraction checks. Its source ZIP also includes this documentation. The repository adds portable fixture discovery and documentation after the runtime build; no runtime code changed afterward.

Starting with v1.0.1, packaging refreshes the Windows ZIP's local `README.md` from `docs/PROGRAM-README.md` and builds `PROGRAM-GUIDE.md` from the operator guide plus operator-facing recovery instructions. It also copies `Open Guides in VS Code.cmd`. Check both Markdown files' relative links and headings in the extracted package. The program README links deliberately target package-local filenames, so check them in the package rather than treating `docs/PROGRAM-README.md` as a repository navigation page. Source ZIPs include `AGENTS.md` and the guide opener as well as the full docs folder.

## Test the actual package

With the private `Hoeganaes23217.rph` fixture available:

```powershell
.\.venv\Scripts\python.exe verify_graph_package.py '.\outputs\graph-extracted-release\Dauch EAF Graph Viewer\engine\EAFGraphEngine.exe'
```

This launches the bundled engine, uploads the real recording and five modified comparison variants, plots every one of the 644 signals, checks individual and overlaid presets, checks line thickness/chart modes, rejects truncation, and restarts to verify saved views. The variants derive from real plant data and remain private local test inputs; they are never release assets.

For the launcher drop integration, compile `test_graph_drop.cs` **beside the extracted launcher** because the launcher resolves `engine` relative to its application base directory:

```powershell
$appFolder = Join-Path $PWD 'outputs\graph-extracted-release\Dauch EAF Graph Viewer'
& "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:exe "/out:$appFolder\DropCheck.exe" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll test_graph_drop.cs
$recordingPaths = Get-ChildItem -LiteralPath $env:EAF_RPH_DIR -Filter '*.rph' | Select-Object -First 6 -ExpandProperty FullName
& "$appFolder\DropCheck.exe" "$appFolder\Dauch EAF Graph Viewer.exe" "$PWD\outputs\drop-test-settings" @recordingPaths
```

Use distinct recording contents. The harness compares loaded file count with the number passed. It injects WinForms drag events and runs the real launcher/engine; it is not a physical mouse-drag test. It opens browser tabs through the normal launcher behavior. The harness must not ship in release assets.

## Browser acceptance checks

Use an isolated `--views` folder and the packaged engine. Verify five-file overlays and each starter view; add ten pins and reject the eleventh; remove/select/clear pins; test Live cursor; zoom/pan/reset; ensure drag and double-click do not add pins. Verify exact captured values remain unchanged across zoom, thickness and chart-style changes.

Check right-only and dual-axis views, UTC and elapsed time, file navigation/filtering, empty selections, missing signals, and error messages. Rapidly change chart styles and filters to check stale-render handling. Deliberately exceed the plot limit and verify the old chart is hidden. Check no page overflow at the intended display size and inspect browser errors. Capture a screenshot locally; do not publish screenshots containing real plant data by default.

## Publish a release

Review staged files for recordings, generated output, secrets, and local paths. Commit source/docs, tag the tested revision, and upload the Windows ZIP, source ZIP and a SHA-256 manifest to a private GitHub release. Verify the remote commit, release tag, uploaded sizes and downloaded checksum. Record any code-versus-runtime differences in the release notes. Keep original ZIPs for rollback.
