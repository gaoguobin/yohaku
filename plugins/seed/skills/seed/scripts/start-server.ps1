#Requires -Version 5.1
[CmdletBinding()]
param(
  [string]$ProjectDir = "",
  [Alias("Host")]
  [string]$BindHost = "127.0.0.1",
  [string]$UrlHost = "",
  [switch]$Foreground,
  [switch]$Background
)

# Start the seed visual companion server and output connection info.
# Usage: .\start-server.ps1 [-ProjectDir <path>] [-Host <bind-host>] [-UrlHost <display-host>] [-Foreground] [-Background]

function Write-JsonLine {
  param([hashtable]$Data)
  $Data | ConvertTo-Json -Compress
}

function Test-ProcessAlive {
  param([int]$ProcessId)
  $null -ne (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue)
}

function Get-LogTail {
  param([string]$Path)
  if (-not (Test-Path $Path)) {
    return ""
  }
  return ((Get-Content -Path $Path -Tail 20 -ErrorAction SilentlyContinue) -join "`n")
}

function Get-OwnerPid {
  try {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $PID" -ErrorAction Stop
    if ($process.ParentProcessId -and $process.ParentProcessId -ne 1) {
      return [string]$process.ParentProcessId
    }
  } catch {
    return ""
  }
  return ""
}

function Set-SeedEnvironment {
  param([hashtable]$Values)

  $previous = @{}
  foreach ($key in $Values.Keys) {
    $previous[$key] = [System.Environment]::GetEnvironmentVariable($key, "Process")
    [System.Environment]::SetEnvironmentVariable($key, [string]$Values[$key], "Process")
  }
  return $previous
}

function Restore-SeedEnvironment {
  param([hashtable]$Previous)

  foreach ($key in $Previous.Keys) {
    [System.Environment]::SetEnvironmentVariable($key, $Previous[$key], "Process")
  }
}

if ([string]::IsNullOrWhiteSpace($UrlHost)) {
  if ($BindHost -eq "127.0.0.1" -or $BindHost -eq "localhost") {
    $UrlHost = "localhost"
  } else {
    $UrlHost = $BindHost
  }
}

$runForeground = $Foreground.IsPresent
if ($env:CODEX_CI -and -not $runForeground -and -not $Background.IsPresent) {
  $runForeground = $true
}

$scriptDir = $PSScriptRoot
$unixEpoch = [datetime]::SpecifyKind([datetime]"1970-01-01T00:00:00Z", [System.DateTimeKind]::Utc)
$timestamp = [int64][System.Math]::Floor(([datetime]::UtcNow - $unixEpoch).TotalSeconds)
$sessionId = "$PID-$timestamp"

if ([string]::IsNullOrWhiteSpace($ProjectDir)) {
  $sessionDir = Join-Path ([System.IO.Path]::GetTempPath()) ("seed-" + $sessionId)
} else {
  $sessionDir = Join-Path (Join-Path (Join-Path $ProjectDir ".seed") "visual") $sessionId
}

$stateDir = Join-Path $sessionDir "state"
$pidFile = Join-Path $stateDir "server.pid"
$logFile = Join-Path $stateDir "server.log"
$errFile = Join-Path $stateDir "server.err.log"

New-Item -ItemType Directory -Force -Path (Join-Path $sessionDir "content"), $stateDir | Out-Null

if (Test-Path $pidFile) {
  $oldPidText = (Get-Content -Path $pidFile -Raw).Trim()
  $oldPid = 0
  if ([int]::TryParse($oldPidText, [ref]$oldPid)) {
    Stop-Process -Id $oldPid -ErrorAction SilentlyContinue
  }
  Remove-Item -Path $pidFile -Force -ErrorAction SilentlyContinue
}

$seedEnv = @{
  SEED_DIR = $sessionDir
  SEED_HOST = $BindHost
  SEED_URL_HOST = $UrlHost
}

$ownerPid = Get-OwnerPid
if (-not [string]::IsNullOrWhiteSpace($ownerPid)) {
  $seedEnv["SEED_OWNER_PID"] = $ownerPid
}

$previousEnv = Set-SeedEnvironment $seedEnv
try {
  if ($runForeground) {
    try {
      $process = Start-Process -FilePath "node" -ArgumentList @("server.cjs") -WorkingDirectory $scriptDir -NoNewWindow -PassThru -ErrorAction Stop
    } catch {
      Write-JsonLine @{ error = "Failed to start server: $($_.Exception.Message)" }
      exit 1
    }
    Set-Content -Path $pidFile -Value $process.Id -Encoding ascii
    $process.WaitForExit()
    exit $process.ExitCode
  }

  try {
    $process = Start-Process -FilePath "node" -ArgumentList @("server.cjs") -WorkingDirectory $scriptDir -RedirectStandardOutput $logFile -RedirectStandardError $errFile -PassThru -ErrorAction Stop
  } catch {
    Write-JsonLine @{ error = "Failed to start server: $($_.Exception.Message)" }
    exit 1
  }

  Set-Content -Path $pidFile -Value $process.Id -Encoding ascii

  for ($i = 0; $i -lt 150; $i++) {
    if ((Test-Path $logFile) -and (Select-String -Path $logFile -Pattern "server-started" -Quiet)) {
      $alive = $true
      for ($j = 0; $j -lt 20; $j++) {
        if (-not (Test-ProcessAlive $process.Id)) {
          $alive = $false
          break
        }
        Start-Sleep -Milliseconds 100
      }

      if (-not $alive) {
        $retry = "$scriptDir\start-server.ps1 -ProjectDir $ProjectDir -Host $BindHost -UrlHost $UrlHost -Foreground"
        Write-JsonLine @{ error = "Server started but was killed. Retry in a persistent PowerShell tool call with: $retry" }
        exit 1
      }

      Get-Content -Path $logFile | Where-Object { $_ -match "server-started" } | Select-Object -First 1
      exit 0
    }
    Start-Sleep -Milliseconds 100
  }

  $alive = Test-ProcessAlive $process.Id
  Write-JsonLine @{
    error = "Server failed to start within 15 seconds"
    process_alive = $alive
    stdout_tail = Get-LogTail $logFile
    stderr_tail = Get-LogTail $errFile
  }
  exit 1
} finally {
  Restore-SeedEnvironment $previousEnv
}
