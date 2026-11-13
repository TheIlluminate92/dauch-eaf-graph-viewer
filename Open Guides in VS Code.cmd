@echo off
setlocal
where code >nul 2>nul
if not errorlevel 1 (
    call code --new-window "%~dp0README.md" "%~dp0PROGRAM-GUIDE.md"
    exit /b
)
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd" (
    call "%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd" --new-window "%~dp0README.md" "%~dp0PROGRAM-GUIDE.md"
    exit /b
)
if exist "%ProgramFiles%\Microsoft VS Code\bin\code.cmd" (
    call "%ProgramFiles%\Microsoft VS Code\bin\code.cmd" --new-window "%~dp0README.md" "%~dp0PROGRAM-GUIDE.md"
    exit /b
)
echo VS Code was not found. Open README.md and PROGRAM-GUIDE.md in your text editor.
echo VS Code is optional; you can run Dauch EAF Graph Viewer.exe without it.
pause
