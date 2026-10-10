param([switch]$Fetch)
$ErrorActionPreference = 'Stop'
$destination = Join-Path $PSScriptRoot '../../application/online-boutique'
$destination = [System.IO.Path]::GetFullPath($destination)
$expectedPrefix = '5b608cb' # Google release v0.10.7; verify the full SHA locally before use.
if (-not $Fetch) {
  Write-Output "Pinned upstream target: https://github.com/GoogleCloudPlatform/microservices-demo tag v0.10.7 (commit prefix $expectedPrefix)."
  Write-Output 'No network fetch was attempted. Re-run with -Fetch when GitHub is reachable.'
  return
}
$repository = 'https://github.com/GoogleCloudPlatform/microservices-demo.git'
if (Test-Path -LiteralPath $destination) {
  if (-not (Test-Path -LiteralPath (Join-Path $destination '.git'))) {
    throw "Path exists but is not a Git checkout; refusing to overwrite: $destination"
  }
  $existingOrigin = (git -C $destination remote get-url origin).Trim()
  if ($LASTEXITCODE -ne 0 -or $existingOrigin -ne $repository) {
    throw "Existing checkout origin does not match the expected upstream repository: $destination"
  }
  $existingSha = (git -C $destination rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0 -or -not $existingSha.StartsWith($expectedPrefix)) {
    throw "Existing checkout SHA does not match upstream v0.10.7 ($expectedPrefix): $existingSha"
  }
  Write-Output "Upstream already present at pinned v0.10.7 commit $existingSha; no fetch or overwrite needed."
  return
}
New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
git clone --depth 1 --branch v0.10.7 $repository $destination
if ($LASTEXITCODE -ne 0) { throw 'Upstream clone failed; remove the incomplete destination and retry.' }
$sha = (git -C $destination rev-parse HEAD).Trim()
if (-not $sha.StartsWith($expectedPrefix)) { throw "Fetched SHA $sha does not match expected release prefix $expectedPrefix." }
Write-Output "Pinned upstream checkout: $sha"
