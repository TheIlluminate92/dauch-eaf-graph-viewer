"""Package only the application, then extract a fresh copy for release tests."""
from pathlib import Path
import shutil
import zipfile

root = Path(__file__).resolve().parent
app = root / 'release' / 'graph-final' / 'Dauch EAF Graph Viewer'
bundle = root / 'Dauch_EAF_Graph_Viewer_Windows.zip'
if not (app / 'Dauch EAF Graph Viewer.exe').is_file() or not (app / 'engine' / 'EAFGraphEngine.exe').is_file():
    raise SystemExit('Build the Windows application before packaging: run build_graph_viewer.ps1.')
# Ship an offline program manual, not the repository/developer README.
shutil.copyfile(root / 'docs' / 'PROGRAM-README.md', app / 'README.md')
shutil.copyfile(root / 'Open Guides in VS Code.cmd', app / 'Open Guides in VS Code.cmd')
guide = (root / 'docs' / 'USER_GUIDE.md').read_text(encoding='utf-8')
guide = guide.replace('# Operator guide', '# Dauch EAF Graph Viewer — program walkthrough', 1)
guide = guide.replace('\n\n', '\n\n[Back to the local README](README.md) · In VS Code, press **Ctrl+Shift+V** for formatted preview.\n\n', 1)
operations = (root / 'docs' / 'OPERATIONS.md').read_text(encoding='utf-8')
# Include operator recovery instructions locally without maintainer-only links.
operations = operations.split('## Diagnose a report')[0]
operations = operations.replace('Then either repair the JSON using the [saved-view reference](SAVED-VIEWS.md), restore a known-good backup, or rename the damaged file and reopen the app for a fresh list.', 'Then restore a known-good backup, or rename the damaged file and reopen the app for a fresh list. Ask a maintainer for help before manually editing the JSON.')
operations = operations.replace('# Troubleshooting and recovery', '## Troubleshooting and recovery', 1)
for heading in ('Startup and loading', 'Back up and recover saved views', 'Roll back the application'):
    operations = operations.replace('## ' + heading, '### ' + heading)
(app / 'PROGRAM-GUIDE.md').write_text(guide + '\n\n' + operations, encoding='utf-8')
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
           'README.md', 'CHANGELOG.md', 'AGENTS.md', 'Open Guides in VS Code.cmd', '.gitignore']
with zipfile.ZipFile(root / 'Dauch_EAF_Graph_Viewer_Source.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for name in sources:
        z.write(root / name, name)
    for path in sorted((root / 'docs').glob('*.md')):
        z.write(path, path.relative_to(root))
print(f'Created {bundle.name} ({bundle.stat().st_size / 1024**2:.1f} MB) and source ZIP; fresh extraction ready.')
