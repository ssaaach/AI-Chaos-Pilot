[CmdletBinding(SupportsShouldProcess=$true, ConfirmImpact='High')]
param(
  [Parameter(Mandatory=$true)][ValidateSet('bosch-ananya')][string]$Cluster,
  [switch]$DeletePvcData
)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command kind -ErrorAction SilentlyContinue)) { throw 'kind is required; no cleanup was attempted.' }
$context = "kind-$Cluster"
$clusters = @(kind get clusters)
if ($LASTEXITCODE -ne 0) { throw 'Unable to query kind clusters; no cleanup was attempted.' }
if ($clusters -notcontains $Cluster) { Write-Output "Owned cluster '$Cluster' is absent."; return }
$labExists = $false
$pvcNames = @()
kubectl --context $context get namespace inventory-lab -o name 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  $labExists = $true
  $pvcNames = @(kubectl --context $context -n inventory-lab get pvc -o name)
  if ($LASTEXITCODE -ne 0) { throw 'Could not inspect lab PVCs; no cleanup was attempted.' }
}
if ($pvcNames.Count -gt 0 -and -not $DeletePvcData) {
  throw "PVCs exist in inventory-lab ($($pvcNames -join ', ')). Pass -DeletePvcData to authorize their deletion before cluster teardown."
}
if ($pvcNames.Count -gt 0 -and -not $PSCmdlet.ShouldProcess("PVCs in $context/inventory-lab: $($pvcNames -join ', ')", 'Delete persistent lab data')) {
  throw 'Persistent lab data deletion was declined; cluster teardown was cancelled.'
}
if (-not $PSCmdlet.ShouldProcess("owned kind cluster $Cluster", 'Delete cluster')) { return }

if ($pvcNames.Count -gt 0) {
  kubectl --context $context -n inventory-lab delete pvc --all --wait=true
  if ($LASTEXITCODE -ne 0) { throw 'PVC deletion failed; cluster retained.' }
}
kubectl --context $context get namespace boutique -o name 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  kubectl --context $context delete namespace boutique --wait=true
  if ($LASTEXITCODE -ne 0) { throw 'Could not remove boutique namespace; cluster retained.' }
}
if ($labExists) {
  kubectl --context $context delete namespace inventory-lab --wait=true
  if ($LASTEXITCODE -ne 0) { throw 'Could not remove inventory-lab namespace; cluster retained.' }
}
kind delete cluster --name $Cluster
if ($LASTEXITCODE -ne 0) { throw 'kind cluster deletion failed.' }
