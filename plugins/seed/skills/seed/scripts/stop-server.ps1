#Requires -Version 5.1
[CmdletBinding()]
param(
  [Parameter(Position = 0)]
  [string]$SessionDir = ""
)

# Stop the seed visual companion server and clean up.
# Usage: .\stop-server.ps1 <session_dir>

function Write-JsonLine {
  param([hashtable]$Data)
  $Data | ConvertTo-Json -Compress
}

function Test-ProcessAlive {
  param([int]$ProcessId)
  $null -ne (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue)
}

if ([string]::IsNullOrWhiteSpace($SessionDir)) {
  Write-JsonLine @{ error = "Usage: stop-server.ps1 <session_dir>" }
  exit 1
}

$stateDir = Join-Path $SessionDir "state"
$pidFile = Join-Path $stateDir "server.pid"
$logFile = Join-Path $stateDir "server.log"
$errFile = Join-Path $stateDir "server.err.log"

if (-not (Test-Path $pidFile)) {
  Write-JsonLine @{ status = "not_running" }
  exit 0
}

$pidText = (Get-Content -Path $pidFile -Raw).Trim()
$serverPid = 0
if (-not [int]::TryParse($pidText, [ref]$serverPid)) {
  Write-JsonLine @{ status = "failed"; error = "invalid pid file" }
  exit 1
}

Stop-Process -Id $serverPid -ErrorAction SilentlyContinue

for ($i = 0; $i -lt 20; $i++) {
  if (-not (Test-ProcessAlive $serverPid)) {
    break
  }
  Start-Sleep -Milliseconds 100
}

if (Test-ProcessAlive $serverPid) {
  Stop-Process -Id $serverPid -Force -ErrorAction SilentlyContinue
  Start-Sleep -Milliseconds 100
}

if (Test-ProcessAlive $serverPid) {
  Write-JsonLine @{ status = "failed"; error = "process still running" }
  exit 1
}

Remove-Item -Path $pidFile, $logFile, $errFile -Force -ErrorAction SilentlyContinue

try {
  $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
  $fullSession = [System.IO.Path]::GetFullPath($SessionDir)
  if ($fullSession.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    Remove-Item -Path $SessionDir -Recurse -Force -ErrorAction SilentlyContinue
  }
} catch {
  # Cleanup is best-effort; stopping the process is the important part.
}

Write-JsonLine @{ status = "stopped" }
