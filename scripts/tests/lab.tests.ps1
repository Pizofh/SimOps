#requires -Version 5.1
# Run from the repository root: powershell -File scripts/tests/lab.tests.ps1
# Uses isolated files and mocked Docker/HTTP; never stops real containers.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$artifactRoot = Join-Path $repoRoot 'artifacts/lab'
$testRoot = Join-Path $artifactRoot "tool-tests-$([guid]::NewGuid().ToString('N'))"
$testScript = Join-Path $testRoot 'scripts/lab.ps1'
New-Item -ItemType Directory -Path (Join-Path $testRoot 'scripts'), (Join-Path $testRoot 'docs/incidents') -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot 'scripts/lab.ps1') -Destination $testScript
Copy-Item -LiteralPath (Join-Path $repoRoot 'docs/postmortem-template.md') -Destination (Join-Path $testRoot 'docs/postmortem-template.md')

$global:SimOpsLabTestState = $null

function Reset-TestState {
    param([string]$Mode = 'normal')
    $global:SimOpsLabTestState = @{
        Mode = $Mode
        Stopped = $false
        Target = ''
        Calls = [Collections.Generic.List[string]]::new()
    }
}

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw "Assertion failed: $Message" }
}

function docker {
    $dockerArgs = @($args)
    $global:LASTEXITCODE = 0
    $global:SimOpsLabTestState.Calls.Add($dockerArgs -join ' ')
    # compose --project-directory <root> -f <file> <command> ...
    $command = $dockerArgs[5]
    switch ($command) {
        'port' { '0.0.0.0:18000' }
        'ps' {
            if ('--services' -in $dockerArgs) {
                @('db', 'backend', 'simulator', 'frontend', 'prometheus', 'loki', 'promtail', 'grafana') |
                    Where-Object {
                        -not ($global:SimOpsLabTestState.Mode -eq 'missing-service' -and $_ -eq 'promtail') -and
                        -not ($global:SimOpsLabTestState.Stopped -and $_ -eq $global:SimOpsLabTestState.Target)
                    }
            } else { 'Mock Compose status' }
        }
        'logs' { 'Mock application log' }
        'stop' {
            $global:SimOpsLabTestState.Stopped = $true
            $global:SimOpsLabTestState.Target = $dockerArgs[-1]
            if ($global:SimOpsLabTestState.Mode -eq 'stop-fails') {
                $global:LASTEXITCODE = 1
                'Mock partial stop failure'
            }
        }
        'start' {
            if ($global:SimOpsLabTestState.Mode -eq 'start-fails') {
                $global:LASTEXITCODE = 1
                'Mock start failure'
            } else { $global:SimOpsLabTestState.Stopped = $false }
        }
        default { throw "Unexpected Docker command: $command" }
    }
}

function Invoke-WebRequest {
    param([string]$Uri, [switch]$UseBasicParsing, [int]$TimeoutSec, [hashtable]$Headers)
    if ($global:SimOpsLabTestState.Mode -eq 'connection-error') {
        throw [Net.WebException]::new('Mock connection refused')
    }
    if ($global:SimOpsLabTestState.Stopped -and $global:SimOpsLabTestState.Target -eq 'backend') {
        throw [Net.WebException]::new('Mock backend unavailable')
    }
    $status = 200
    if ($global:SimOpsLabTestState.Mode -eq 'not-ready' -and $Uri.EndsWith('/ready')) { $status = 503 }
    if ($global:SimOpsLabTestState.Stopped -and $global:SimOpsLabTestState.Target -eq 'db' -and
        ($Uri.EndsWith('/ready') -or $Uri.Contains('/events'))) { $status = 503 }
    [pscustomobject]@{ StatusCode = $status; Content = '{"mock":true}' }
}

function Start-Sleep { param([int]$Seconds) }

try {
    foreach ($scenario in @('database-down', 'backend-down', 'simulator-down', 'logs-down')) {
        Reset-TestState
        & $testScript -Action Drill -Scenario $scenario -DurationSeconds 15 | Out-Null
        $stops = @($global:SimOpsLabTestState.Calls | Where-Object { $_ -match ' stop --timeout 5 ' })
        $starts = @($global:SimOpsLabTestState.Calls | Where-Object { $_ -match ' start ' })
        Assert-True ($stops.Count -eq 1 -and $starts.Count -eq 1) "$scenario must stop and start exactly one service"
        Assert-True (-not $global:SimOpsLabTestState.Stopped) "$scenario must restore the service"
        Assert-True ($stops[0].Split(' ')[-1] -eq $starts[0].Split(' ')[-1]) 'Recovery must target the same service'
    }
    $sessions = @(Get-ChildItem -LiteralPath (Join-Path $testRoot 'artifacts/lab') -Directory)
    Assert-True ($sessions.Count -eq 4) 'Four drills must produce four evidence directories'
    foreach ($session in $sessions) {
        $timeline = Get-Content -LiteralPath (Join-Path $session.FullName 'timeline.txt') -Raw
        Assert-True ($timeline.Contains('stop_completed') -and $timeline.Contains('start_completed') -and
            $timeline.Contains('recovery_checks_passed')) 'Timeline must record fault and verified partial recovery'
        foreach ($phase in @('before', 'during', 'after')) {
            $probes = Get-Content -LiteralPath (Join-Path $session.FullName "$phase/http.json") -Raw | ConvertFrom-Json
            Assert-True ($probes.Count -eq 4) 'Each snapshot must contain four probes'
            Assert-True ($probes[0].uri -eq 'http://127.0.0.1:18000/health') 'Discover a custom published backend port'
            if ($phase -eq 'during' -and $session.Name -like '*-database-down-*') {
                Assert-True ($probes[0].status_code -eq 200 -and $probes[1].status_code -eq 503) 'Database failure must preserve liveness and capture readiness failure'
            }
            if ($phase -eq 'during' -and $session.Name -like '*-backend-down-*') {
                Assert-True ($null -eq $probes[0].status_code -and $probes[0].error -like '*unavailable*') 'Backend outage must capture connection errors'
            }
        }
    }
    $drafts = @(Get-ChildItem -LiteralPath (Join-Path $testRoot 'docs/incidents') -Filter '*.md')
    Assert-True ($drafts.Count -eq 4) 'Each drill must create a postmortem draft'
    foreach ($draft in $drafts) {
        Assert-True (-not (Get-Content -LiteralPath $draft.FullName -Raw -Encoding UTF8).Contains('{{')) 'Template tokens must be replaced'
    }
    Write-Host 'PASS: four scenarios, automatic restoration, evidence, custom port and postmortems'

    foreach ($mode in @('missing-service', 'not-ready')) {
        Reset-TestState -Mode $mode
        $failure = $null
        try { & $testScript -Action Drill -DurationSeconds 15 | Out-Null } catch { $failure = $_ }
        Assert-True ($null -ne $failure) "$mode must reject the drill"
        Assert-True (@($global:SimOpsLabTestState.Calls | Where-Object { $_ -match ' stop ' }).Count -eq 0) 'Preflight failure must not stop anything'
    }
    Write-Host 'PASS: unhealthy or incomplete baseline rejected without mutations'

    Reset-TestState -Mode 'stop-fails'
    $failure = $null
    try { & $testScript -Action Drill -DurationSeconds 15 | Out-Null } catch { $failure = $_ }
    Assert-True ($null -ne $failure) 'Partial stop failure must be reported'
    Assert-True (-not $global:SimOpsLabTestState.Stopped) 'Partial stop failure must still attempt restoration'
    Write-Host 'PASS: restoration after partial stop failure'

    Reset-TestState -Mode 'start-fails'
    $failure = $null
    try { & $testScript -Action Drill -DurationSeconds 15 | Out-Null } catch { $failure = $_ }
    Assert-True ($null -ne $failure -and $global:SimOpsLabTestState.Stopped) 'Start failure must be reported, not claimed as recovery'
    Write-Host 'PASS: recovery failure is visible'

    Reset-TestState -Mode 'connection-error'
    & $testScript -Action Snapshot | Out-Null
    $manual = @(Get-ChildItem -LiteralPath (Join-Path $testRoot 'artifacts/lab') -Directory | Where-Object {
        Test-Path -LiteralPath (Join-Path $_.FullName 'manual/http.json')
    })
    $probes = Get-Content -LiteralPath (Join-Path $manual[-1].FullName 'manual/http.json') -Raw | ConvertFrom-Json
    Assert-True ($probes[0].error -like '*connection refused*') 'Connection failure must be captured as evidence'
    Write-Host 'PASS: HTTP connection failure captured'

    Reset-TestState
    & $testScript -Action NewPostmortem | Out-Null
    Assert-True ($global:SimOpsLabTestState.Calls.Count -eq 0) 'Creating a postmortem must not access Docker'
    Write-Host 'PASS: independent postmortem creation'
} finally {
    # Only remove this test's generated tree after validating its resolved location.
    $resolvedTestRoot = [IO.Path]::GetFullPath($testRoot)
    $allowedPrefix = [IO.Path]::GetFullPath($artifactRoot) + [IO.Path]::DirectorySeparatorChar
    if (-not $resolvedTestRoot.StartsWith($allowedPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing cleanup outside test artifacts: $resolvedTestRoot"
    }
    Remove-Item -LiteralPath $resolvedTestRoot -Recurse -Force
    Remove-Variable -Name SimOpsLabTestState -Scope Global
}
