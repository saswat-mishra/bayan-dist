@echo off
REM Bayan - start the gate and the operator console.
REM   run.bat              start both (gate :8787, console :5173)
REM   run.bat --gate-only  start only the gate
REM   run.bat --reseed     rebuild the demo dataset first
setlocal enabledelayedexpansion
cd /d "%~dp0"

if "%GATE_PORT%"=="" set GATE_PORT=8787
if "%UI_PORT%"==""   set UI_PORT=5173
if "%DATA_DIR%"==""  set DATA_DIR=var
set GATE_ONLY=0
set RESEED=0
for %%A in (%*) do (
  if /i "%%A"=="--gate-only" set GATE_ONLY=1
  if /i "%%A"=="--reseed"    set RESEED=1
)

echo.
echo  Bayan
echo  =====

REM ---------------------------------------------------------------- prerequisites
REM cmd does not treat ^ as an escape inside quotes, so a ">=" comparison in a
REM -c string is unreliable. min()/== avoids angle brackets entirely.
set "PYEXE="
where python >nul 2>&1 && set "PYEXE=python"
if not defined PYEXE (
  where py >nul 2>&1 && set "PYEXE=py"
)
if not defined PYEXE (
  echo  ERROR: Python not found on PATH. Install Python 3.11+ and re-run.
  exit /b 1
)
%PYEXE% -c "import sys;raise SystemExit(0 if min(sys.version_info[:2],(3,11))==(3,11) else 1)"
if errorlevel 1 (
  echo  ERROR: Python 3.11 or newer is required.
  %PYEXE% --version
  exit /b 1
)
if "%GATE_ONLY%"=="0" (
  where npm >nul 2>&1
  if errorlevel 1 (
    echo  ERROR: Node.js / npm not found on PATH. Install Node 20+, or run: run.bat --gate-only
    exit /b 1
  )
)


REM ---------------------------------------------------------------- ports
netstat -ano | findstr /r /c:":%GATE_PORT% .*LISTENING" >nul 2>&1
if not errorlevel 1 (
  echo  ERROR: Port %GATE_PORT% is already in use. Stop whatever is using it, or set
  echo         different ports:  set GATE_PORT=8788 ^& set UI_PORT=5174 ^& run.bat
  exit /b 1
)
netstat -ano | findstr /r /c:":%UI_PORT% .*LISTENING" >nul 2>&1
if not errorlevel 1 (
  echo  ERROR: Port %UI_PORT% is already in use. Stop whatever is using it, or set
  echo         different ports:  set GATE_PORT=8788 ^& set UI_PORT=5174 ^& run.bat
  exit /b 1
)

REM ---------------------------------------------------------------- python deps
if not exist ".venv" (
  echo  creating .venv
  %PYEXE% -m venv .venv
  if errorlevel 1 exit /b 1
)
if not exist ".venv\.deps-installed" (
  echo  installing python packages
  ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  ".venv\Scripts\python.exe" -m pip install --quiet -e .
  if errorlevel 1 exit /b 1
  ".venv\Scripts\python.exe" scripts\dev_pth.py >nul 2>&1
  echo ok> ".venv\.deps-installed"
)

REM ---------------------------------------------------------------- seed
if "%RESEED%"=="1" (
  echo  removing %DATA_DIR% for a clean reseed
  if exist "%DATA_DIR%" rmdir /s /q "%DATA_DIR%"
)
if not exist "%DATA_DIR%" (
  echo  seeding the demo dataset ^(50,000 fingerprints, 10-20s^)
  ".venv\Scripts\python.exe" scripts\seed.py --data-dir "%DATA_DIR%"
  if errorlevel 1 exit /b 1
) else (
  echo  using existing dataset in %DATA_DIR%\  ^(--reseed to rebuild^)
)

REM ---------------------------------------------------------------- node deps
if "%GATE_ONLY%"=="0" (
  if not exist "packages\ui\node_modules" (
    echo  installing console dependencies ^(first run, may take a minute^)
    pushd packages\ui
    call npm install --no-audit --no-fund
    popd
  )
)

REM ---------------------------------------------------------------- run
echo  starting gate on http://127.0.0.1:%GATE_PORT%
start "Bayan gate" cmd /k ""%CD%\.venv\Scripts\python.exe" -m bayan_gate.main --data-dir "%DATA_DIR%" --port %GATE_PORT%"

if "%GATE_ONLY%"=="1" (
  echo.
  echo   Gate    http://127.0.0.1:%GATE_PORT%
  echo.
  echo  The gate runs in its own window. Close that window to stop it.
  exit /b 0
)

echo  waiting for the gate to come up
timeout /t 8 /nobreak >nul

echo  starting console on http://127.0.0.1:%UI_PORT%
start "Bayan console" cmd /k "cd /d "%CD%\packages\ui" && set "BAYAN_GATE=http://127.0.0.1:%GATE_PORT%" && npm run dev -- --port %UI_PORT%"

timeout /t 5 /nobreak >nul
start "" http://127.0.0.1:%UI_PORT%

echo.
echo   Console   http://127.0.0.1:%UI_PORT%
echo   Gate      http://127.0.0.1:%GATE_PORT%
echo.
echo  Switch "Acting as" between Omar (engineer), Layla and Faisal (reviewers),
echo  Priya (delivery lead) and Khalid (auditor).
echo  Each service runs in its own window; close a window to stop it.
exit /b 0
