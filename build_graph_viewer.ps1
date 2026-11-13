# Build the Windows launcher and bundled local engine. Run from the project folder.
$ErrorActionPreference = 'Stop'
$projectFolder = $PSScriptRoot
$pythonExe = Join-Path $projectFolder '.venv\Scripts\python.exe'
$outputFolder = Join-Path $projectFolder 'release\graph-final'
$appFolder = Join-Path $outputFolder 'Dauch EAF Graph Viewer'
$pageFile = Join-Path $projectFolder 'viewer.html'
$cursorFile = Join-Path $projectFolder 'cursor_tools.js'
New-Item -ItemType Directory -Force -Path $appFolder | Out-Null
& $pythonExe -m PyInstaller --noconfirm --onedir --name EAFGraphEngine --distpath (Join-Path $outputFolder 'bundled') --workpath (Join-Path $projectFolder 'build\graph') --specpath (Join-Path $projectFolder 'build') --add-data "$pageFile;." --add-data "$cursorFile;." --collect-data plotly --exclude-module matplotlib --exclude-module scipy --exclude-module statsmodels --exclude-module IPython --exclude-module tkinter --exclude-module pymssql --exclude-module pyarrow --exclude-module nbformat (Join-Path $projectFolder 'graph_viewer.py')
if ($LASTEXITCODE -ne 0) { throw 'Engine build failed.' }
# Copy contents, not the parent directory, so rebuilding cannot nest engine folders.
$engineFolder = Join-Path $appFolder 'engine'
New-Item -ItemType Directory -Force -Path $engineFolder | Out-Null
Copy-Item -Path (Join-Path $outputFolder 'bundled\EAFGraphEngine\*') -Destination $engineFolder -Recurse -Force
& "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:winexe "/out:$appFolder\Dauch EAF Graph Viewer.exe" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll (Join-Path $projectFolder 'EAFGraphViewer.cs')
if ($LASTEXITCODE -ne 0) { throw 'Launcher build failed.' }
Copy-Item -LiteralPath (Join-Path $projectFolder 'GRAPH VIEWER - START HERE.txt') -Destination (Join-Path $appFolder 'START HERE.txt') -Force
Write-Output "Built: $appFolder"
