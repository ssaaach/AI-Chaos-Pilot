param(
  [Parameter(Mandatory=$true)][ValidateSet('kind-bosch-ananya')][string]$Context,
  [string]$SandboxId = 'bosch-ananya',
  [string[]]$Namespaces = @('boutique','inventory-lab','resilience-system'),
  [string]$OutputPath = 'sandbox.identity.json'
)
$ErrorActionPreference = 'Stop'
$config = kubectl --context $Context config view --minify -o json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw "Cannot read explicit context '$Context'." }
$cluster = $config.clusters[0].cluster
$endpoint = [string]$cluster.server
if (-not $endpoint.StartsWith('https://')) { throw 'Refusing to enroll a non-TLS Kubernetes API endpoint.' }
$caBytes = $null
if ($cluster.'certificate-authority-data') {
  $caBytes = [Convert]::FromBase64String($cluster.'certificate-authority-data')
} elseif ($cluster.'certificate-authority') {
  $caPath = [string]$cluster.'certificate-authority'
  if (-not [System.IO.Path]::IsPathRooted($caPath)) { $caPath = Join-Path (Get-Location) $caPath }
  $caBytes = [System.IO.File]::ReadAllBytes($caPath)
} else {
  throw 'Kubeconfig has no inspectable CA certificate; refusing to enroll.'
}
$shaProvider = [System.Security.Cryptography.SHA256]::Create()
try { $sha = $shaProvider.ComputeHash($caBytes) } finally { $shaProvider.Dispose() }
$fingerprint = ([BitConverter]::ToString($sha)).Replace('-', '').ToLowerInvariant()
$uids = @{}
foreach ($namespace in $Namespaces) {
  $ns = kubectl --context $Context get namespace $namespace -o json | ConvertFrom-Json
  if ($LASTEXITCODE -ne 0) { throw "Namespace '$namespace' is absent; create it before enrollment." }
  $uids[$namespace] = [string]$ns.metadata.uid
}
$identity = [ordered]@{
  schema_version = '1.0'
  sandbox_id = $SandboxId
  context = $Context
  api_endpoint = $endpoint
  ca_fingerprint = "sha256:$fingerprint"
  namespace_uids = $uids
  enrolled_at = [DateTime]::UtcNow.ToString('o')
}
$json = $identity | ConvertTo-Json -Depth 5
$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList $false
[System.IO.File]::WriteAllText($resolvedOutput, $json, $utf8NoBom)
Write-Output "Wrote non-secret sandbox identity to $resolvedOutput"
