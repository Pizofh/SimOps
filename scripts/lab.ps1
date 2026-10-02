#requires -Version 5.1
<#
.SYNOPSIS
Captura evidencias y ejecuta fallos reversibles en el Compose local de SimOps.
.EXAMPLE
powershell -File scripts/lab.ps1 -Action Drill -Scenario database-down -DurationSeconds 30
#>
[CmdletBinding()]
param(
    [ValidateSet('Status', 'Snapshot', 'Drill', 'NewPostmortem')]
    [string]$Action = 'Status',
    [ValidateSet('database-down', 'backend-down', 'simulator-down', 'logs-down')]
    [string]$Scenario = 'database-down',
    [ValidateRange(15, 300)]
    [int]$DurationSeconds = 30
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$composeArgs = @('compose', '--project-directory', $repoRoot, '-f', (Join-Path $repoRoot 'docker-compose.yml'))
$sessionId = '{0}-{1}-{2}' -f [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'), $Scenario, [guid]::NewGuid().ToString('N').Substring(0, 8)
$evidenceRoot = Join-Path $repoRoot "artifacts/lab/$sessionId"
$targets = @{
    'database-down' = 'db'
    'backend-down' = 'backend'
    'simulator-down' = 'simulator'
    'logs-down' = 'promtail'
}

function Invoke-Compose {
    param([string[]]$Arguments)
    # Windows PowerShell wraps native stderr in ErrorRecord even for successful commands.
    $previousPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $output = @(& docker @composeArgs @Arguments 2>&1 | ForEach-Object { "$_" })
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousPreference
    }
    if ($exitCode -ne 0) {
        throw "docker compose $($Arguments -join ' ') failed ($exitCode): $($output -join [Environment]::NewLine)"
    }
    return $output
}

function Get-ApiBaseUrl {
    $binding = @(Invoke-Compose -Arguments @('port', 'backend', '8000'))
    foreach ($line in $binding) {
        if ($line -match ':(\d+)$') {
            return "http://127.0.0.1:$($Matches[1])"
        }
    }
    throw 'No published backend port found. Start the stack with docker compose up --build -d.'
}

function Get-Probe {
    param([string]$Uri)
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $result = [ordered]@{
        timestamp_utc = [DateTime]::UtcNow.ToString('o')
        uri = $Uri
        status_code = $null
        duration_ms = 0
        body = $null
        error = $null
    }
    try {
        $response = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 5 -Headers @{
            'X-Request-ID' = "simops-lab-$([guid]::NewGuid().ToString('N'))"
        }
        $result.status_code = [int]$response.StatusCode
        $result.body = [string]$response.Content
    } catch {
        $result.error = $_.Exception.Message
        if ($_.Exception.PSObject.Properties['Response'] -and $_.Exception.Response) {
            $result.status_code = [int]$_.Exception.Response.StatusCode
        }
        if ($_.ErrorDetails) {
            $result.body = $_.ErrorDetails.Message
        }
    }
    $result.duration_ms = $timer.ElapsedMilliseconds
    return [pscustomobject]$result
}

function Write-Timeline {
    param([string]$Event)
    $line = '{0} {1}' -f [DateTime]::UtcNow.ToString('o'), $Event
    try {
        [IO.File]::AppendAllText(
            (Join-Path $evidenceRoot 'timeline.txt'),
            ($line + [Environment]::NewLine),
            [Text.UTF8Encoding]::new($false)
        )
    } catch {
        Write-Warning "Could not write timeline: $($_.Exception.Message)"
    }
    Write-Host $line
}

function Save-Snapshot {
    param([string]$Phase, [string]$ApiBaseUrl)
    $directory = Join-Path $evidenceRoot $Phase
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    [DateTime]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $directory 'timestamp-utc.txt') -Encoding UTF8
    foreach ($capture in @(
        @{ Name = 'compose-ps.txt'; Arguments = @('ps', '--all') },
        @{ Name = 'logs.txt'; Arguments = @('logs', '--no-color', '--timestamps', '--since', '5m', '--tail', '200', 'backend', 'simulator', 'db', 'promtail') }
    )) {
        try {
            Invoke-Compose -Arguments $capture.Arguments | Set-Content -LiteralPath (Join-Path $directory $capture.Name) -Encoding UTF8
        } catch {
            $_.Exception.Message | Set-Content -LiteralPath (Join-Path $directory $capture.Name) -Encoding UTF8
        }
    }
    $probes = @('/health', '/ready', '/events?limit=5', '/metrics') | ForEach-Object {
        Get-Probe -Uri "$ApiBaseUrl$_"
    }
    $probes | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $directory 'http.json') -Encoding UTF8
    Write-Timeline "snapshot=$Phase"
}

function New-Postmortem {
    param([string]$EvidenceLink = 'Pendiente')
    $template = Get-Content -LiteralPath (Join-Path $repoRoot 'docs/postmortem-template.md') -Raw -Encoding UTF8
    $content = $template.Replace('{{TITLE}}', $Scenario).Replace('{{SCENARIO}}', $Scenario).
        Replace('{{CREATED_AT}}', [DateTime]::UtcNow.ToString('o')).Replace('{{EVIDENCE}}', $EvidenceLink)
    $path = Join-Path $repoRoot "docs/incidents/$sessionId.md"
    $content | Set-Content -LiteralPath $path -Encoding UTF8
    Write-Host "Postmortem: $path"
}

if ($Action -eq 'NewPostmortem') {
    New-Postmortem
    return
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker is not available. Install/start Docker Desktop with Linux containers and Docker Compose.'
}
$apiBaseUrl = Get-ApiBaseUrl
if ($Action -eq 'Status') {
    Invoke-Compose -Arguments @('ps', '--all')
    Get-Probe -Uri "$apiBaseUrl/health" | ConvertTo-Json
    Get-Probe -Uri "$apiBaseUrl/ready" | ConvertTo-Json
    return
}

if ($Action -eq 'Drill') {
    $running = @(Invoke-Compose -Arguments @('ps', '--status', 'running', '--services'))
    $required = @('db', 'backend', 'simulator', 'frontend', 'prometheus', 'loki', 'promtail', 'grafana')
    $missing = @($required | Where-Object { $_ -notin $running })
    if ($missing.Count -gt 0) {
        throw "Start the full stack before a drill. Services not running: $($missing -join ', ')"
    }
    if ((Get-Probe -Uri "$apiBaseUrl/ready").status_code -ne 200) {
        throw 'Backend is not ready. Establish a healthy baseline before injecting a fault.'
    }
}

New-Item -ItemType Directory -Path $evidenceRoot -Force | Out-Null
Write-Host "Evidence: $evidenceRoot"
if ($Action -eq 'Snapshot') {
    Save-Snapshot -Phase 'manual' -ApiBaseUrl $apiBaseUrl
    return
}

New-Postmortem -EvidenceLink "[Capturas locales](../../artifacts/lab/$sessionId/)"
@{
    scenario = $Scenario
    target = $targets[$Scenario]
    requested_duration_seconds = $DurationSeconds
    api_base_url = $apiBaseUrl
    created_at_utc = [DateTime]::UtcNow.ToString('o')
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidenceRoot 'exercise.json') -Encoding UTF8
Save-Snapshot -Phase 'before' -ApiBaseUrl $apiBaseUrl
$target = $targets[$Scenario]
$stopAttempted = $false
try {
    # Set before invoking stop: even a partially failed stop requires recovery.
    $stopAttempted = $true
    Write-Timeline "stop_requested service=$target"
    Invoke-Compose -Arguments @('stop', '--timeout', '5', $target) | Out-Host
    Write-Timeline "stop_completed service=$target"
    $faultTimer = [Diagnostics.Stopwatch]::StartNew()
    Save-Snapshot -Phase 'during' -ApiBaseUrl $apiBaseUrl
    $remaining = [Math]::Max(0, [Math]::Ceiling($DurationSeconds - $faultTimer.Elapsed.TotalSeconds))
    Write-Host "Observe Grafana and the frontend. Recovery in approximately $remaining seconds."
    if ($remaining -gt 0) { Start-Sleep -Seconds $remaining }
} finally {
    if ($stopAttempted) {
        Write-Timeline "start_requested service=$target"
        try {
            Invoke-Compose -Arguments @('start', $target) | Out-Host
            Write-Timeline "start_completed service=$target"
        } catch {
            Write-Timeline "recovery_failed service=$target"
            Write-Warning "Manual recovery required: docker compose start $target"
            throw
        }
    }
}

$recoveryTimer = [Diagnostics.Stopwatch]::StartNew()
$recovered = $false
do {
    $running = @(Invoke-Compose -Arguments @('ps', '--status', 'running', '--services'))
    $ready = Get-Probe -Uri "$apiBaseUrl/ready"
    $events = Get-Probe -Uri "$apiBaseUrl/events?limit=1"
    $recovered = ($target -in $running) -and ($ready.status_code -eq 200) -and ($events.status_code -eq 200)
    if (-not $recovered) { Start-Sleep -Seconds 2 }
} while (-not $recovered -and $recoveryTimer.Elapsed.TotalSeconds -lt 60)
Save-Snapshot -Phase 'after' -ApiBaseUrl $apiBaseUrl
if (-not $recovered) {
    Write-Timeline 'recovery_checks_failed'
    throw "Recovery checks did not pass. Inspect evidence and run docker compose start $target if needed."
}
Write-Timeline 'recovery_checks_passed (service running, readiness and event read HTTP 200)'
Write-Host 'Verify new event ingestion and fresh Loki logs, then complete the postmortem using docs/lab.md.'
