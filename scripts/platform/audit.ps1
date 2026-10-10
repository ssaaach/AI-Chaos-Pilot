param(
  [Parameter(Mandatory=$true)][string]$Context,
  [string]$Namespace = 'boutique'
)
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Context)) { throw 'An explicit Kubernetes context is required.' }
$active = (& kubectl config current-context 2>$null)
Write-Output "Requested context: $Context"
Write-Output "Current context: $active"
if ($active -ne $Context) { throw 'Current context differs from requested context; audit stopped.' }

Write-Output "OS: $([System.Environment]::OSVersion.VersionString)"
$computer = Get-CimInstance Win32_ComputerSystem
$totalRamGiB = [Math]::Round($computer.TotalPhysicalMemory / 1GB, 1)
$freeDisk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$((Get-Location).Drive.Name):'"
$freeDiskGiB = if ($freeDisk) { [Math]::Round($freeDisk.FreeSpace / 1GB, 1) } else { 'unknown' }
Write-Output "Memory: $totalRamGiB GiB; free space on workspace drive: $freeDiskGiB GiB"
foreach ($toolName in @('docker','kind','kubectl')) {
  $tool = Get-Command $toolName -ErrorAction SilentlyContinue
  if ($tool) { Write-Output "$toolName executable: $($tool.Source)" }
  else { Write-Output "$toolName executable: NOT FOUND" }
}
docker info --format 'Docker engine: {{.OSType}}/{{.Architecture}}, {{.NCPU}} CPUs, {{.MemTotal}} bytes' 2>$null
if ($LASTEXITCODE -ne 0) { Write-Output 'Docker engine: unavailable' }
kubectl version --client -o yaml

$cluster = (& kubectl --context $Context config view --minify -o json | ConvertFrom-Json)
$endpoint = $cluster.clusters[0].cluster.server
if (-not $endpoint.StartsWith('https://')) { throw 'Refusing non-TLS API endpoint.' }
Write-Output "API endpoint: $endpoint"
kubectl --context $Context get namespace $Namespace -o 'custom-columns=NAME:.metadata.name,UID:.metadata.uid,STATUS:.status.phase'
kubectl --context $Context -n $Namespace get deployments,services,pods -o wide
Write-Output 'This audit is read-only. It does not enroll identity, install tools, or mutate resources.'
