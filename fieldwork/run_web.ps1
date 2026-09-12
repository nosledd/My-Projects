# Launch the interface with the project virtual environment when available.
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$bundledPython = "C:\Users\DELSON\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path -LiteralPath $venvPython) {
    $python = $venvPython
} elseif (Test-Path -LiteralPath $bundledPython) {
    $python = $bundledPython
} else {
    throw "No Python runtime was found. Create .venv and install the project dependencies."
}

$env:PYTHONPATH = Join-Path $projectRoot "src"
& $python (Join-Path $projectRoot "run_web.py")
