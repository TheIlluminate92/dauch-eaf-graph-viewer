"""Package only the application, then extract a fresh copy for release tests."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
app = root / 'release' / 'graph-final' / 'Dauch EAF Graph Viewer'
bundle = root / 'Dauch_EAF_Graph_Viewer_Windows.zip'
if not (app / 'Dauch EAF Graph Viewer.exe').is_file() or not (app / 'engine' / 'EAFGraphEngine.exe').is_file():
    raise SystemExit('Build the Windows application before packaging: run build_graph_viewer.ps1.')
with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in app.rglob('*'):
        if path.is_file() and path.name != 'DropCheck.exe':
            z.write(path, path.relative_to(app.parent))
with zipfile.ZipFile(bundle) as z:
    assert z.testzip() is None
    z.extractall(root / 'outputs' / 'graph-extracted-release')
sources = ['rph_reader.py', 'graph_viewer.py', 'standard_views.py', 'viewer.html', 'cursor_tools.js', 'test_cursor_tools.cjs',
           'EAFGraphViewer.cs', 'test_viewer.py', 'test_graph_drop.cs',
           'verify_graph_package.py', 'build_graph_viewer.ps1',
           'package_graph_viewer.py', 'GRAPH VIEWER - START HERE.txt', 'requirements-graph.txt',
           'README.md', 'CHANGELOG.md', '.gitignore']
with zipfile.ZipFile(root / 'Dauch_EAF_Graph_Viewer_Source.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for name in sources:
        z.write(root / name, name)
    for path in sorted((root / 'docs').glob('*.md')):
        z.write(path, path.relative_to(root))
print(f'Created {bundle.name} ({bundle.stat().st_size / 1024**2:.1f} MB) and source ZIP; fresh extraction ready.')
