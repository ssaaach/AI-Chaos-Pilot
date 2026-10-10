param(
  [Parameter(Mandatory=$true)][ValidateSet('kind-bosch-ananya')][string]$Context,
  [ValidateRange(1024,65535)][int]$LocalPort = 8080
)
$ErrorActionPreference = 'Stop'
kubectl --context $Context -n boutique get service frontend | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'boutique/frontend service is unavailable; port-forward not started.' }
kubectl --context $Context -n boutique port-forward service/frontend "$LocalPort`:80" --address 127.0.0.1
