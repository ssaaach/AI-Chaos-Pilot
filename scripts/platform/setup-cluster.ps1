param([switch]$CreateCluster)
$ErrorActionPreference = 'Stop'
$cluster = 'bosch-ananya'
$context = 'kind-bosch-ananya'

foreach ($toolName in @('docker', 'kubectl', 'kind')) {
  if (-not (Get-Command $toolName -ErrorAction SilentlyContinue)) {
    throw "Required tool '$toolName' is missing. Install it and rerun; this script will not download installers."
  }
}

docker info | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Docker engine is unavailable. Start Docker Desktop and retry.' }
$clusters = @(kind get clusters)
if ($LASTEXITCODE -ne 0) { throw 'Unable to query kind clusters.' }
if ($clusters -contains $cluster) {
  Write-Output "Owned cluster '$cluster' already exists. Verifying its expected context."
  kubectl --context $context get nodes
  if ($LASTEXITCODE -ne 0) { throw "Cluster exists but expected context '$context' is unusable." }
  kubectl --context $context wait --for=condition=Ready nodes --all --timeout=180s
  if ($LASTEXITCODE -ne 0) { throw 'Cluster exists but its nodes are not Ready yet; wait for kind startup and rerun.' }
} elseif ($CreateCluster) {
  kind create cluster --name $cluster --config infrastructure/kind/bosch-ananya.yaml --wait 120s
  if ($LASTEXITCODE -ne 0) { throw 'kind create failed.' }
  kubectl --context $context wait --for=condition=Ready nodes --all --timeout=120s
  if ($LASTEXITCODE -ne 0) { throw 'Cluster nodes did not become Ready.' }
} else {
  throw "Cluster '$cluster' does not exist. Pass -CreateCluster to create this named local cluster."
}

$localManifest = kubectl kustomize --load-restrictor=LoadRestrictionsNone infrastructure/k8s/overlays/local
if ($LASTEXITCODE -ne 0) { throw 'Could not render the local namespace foundation.' }
$localManifest | kubectl --context $context apply -f -
if ($LASTEXITCODE -ne 0) { throw 'Failed applying the local namespace foundation.' }
$upstreamManifest = 'application/online-boutique/release/kubernetes-manifests.yaml'
if (Test-Path -LiteralPath $upstreamManifest) {
  $appManifest = kubectl kustomize --load-restrictor=LoadRestrictionsNone infrastructure/k8s/overlays/online-boutique
  if ($LASTEXITCODE -ne 0) { throw 'Could not render the Online Boutique overlay.' }
  $appManifest | kubectl --context $context apply -f -
  if ($LASTEXITCODE -ne 0) { throw 'Online Boutique deployment failed.' }
  kubectl --context $context -n boutique rollout status deployment/frontend --timeout=180s
  if ($LASTEXITCODE -ne 0) { throw 'Frontend did not become ready.' }
  Write-Output "Online Boutique resources applied on $context; run the functional smoke script before calling it healthy."
} else {
  Write-Output "Prepared namespace foundation on $context. Run scripts/platform/fetch-upstream.ps1 -Fetch, then rerun setup for the full application."
}
