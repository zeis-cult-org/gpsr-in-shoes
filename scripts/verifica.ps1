# Controlli automatici sul portale GPSR (solo lettura, non modifica nulla).
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\verifica.ps1
#       powershell -ExecutionPolicy Bypass -File scripts\verifica.ps1 -SitoUrl https://gpsr.in-shoes.it/
param([string]$SitoUrl = "")

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$root = Split-Path -Parent $PSScriptRoot
$file = Join-Path $root "public\index.html"
$fail = 0
function Ok($m)  { Write-Host "[OK]   $m" -ForegroundColor Green }
function Ko($m)  { Write-Host "[ERRORE] $m" -ForegroundColor Red; $script:fail++ }

$h1 = '<h1>GPSR - Sicurezza dei prodotti.</h1>'
$dest = @(
  'https://www.cultofficial.com/pages/gpsr',
  'https://www.docksteps.com/pages/gpsr',
  'https://www.oxs-shoes.it/pages/gpsr'
)

if (-not (Test-Path $file)) {
  Ko "public\index.html mancante: inserire la pagina approvata."
} else {
  # Impronta della pagina approvata (revisione H1 del 4/11/2026): se cambia, la pagina non e' piu' quella approvata.
  $md5Approvato = "3744F3A5888A95DBCCB14A9249328A0D"
  $md5 = (Get-FileHash $file -Algorithm MD5).Hash
  if ($md5 -eq $md5Approvato) { Ok "index.html identico alla versione approvata (MD5)" }
  else { Ko "index.html diverso dalla versione approvata (MD5 $md5). Se e' una nuova versione approvata, aggiornare md5Approvato." }
  $html = [IO.File]::ReadAllText($file, [Text.Encoding]::UTF8)
  if ($html.Contains($h1)) { Ok "H1 esatto presente" } else { Ko "H1 diverso da quello approvato" }
  foreach ($u in $dest) {
    if ($html.Contains("href=`"$u`"")) { Ok "link presente: $u" } else { Ko "link mancante o diverso: $u" }
  }
  # Ogni URL http(s) nel file deve essere una delle tre destinazioni.
  $altri = [regex]::Matches($html, 'https?://[^"''\s<>)]+') | ForEach-Object { $_.Value } |
           Where-Object { $dest -notcontains $_ } | Sort-Object -Unique
  if ($altri) { Ko ("URL esterni non previsti: " + ($altri -join ", ")) } else { Ok "nessun URL esterno oltre ai tre marchi" }
  if ($html -match '<script[^>]*\bsrc=') { Ko "script esterno trovato" } else { Ok "nessuno script esterno" }
  if ($html -match '(?i)<link[^>]*rel="?stylesheet' -or $html -match '(?i)@import') { Ko "CSS/font esterni trovati" } else { Ok "nessun CSS/font esterno" }
  if ($html -match '(?i)viewport') { Ok "meta viewport presente (mobile)" } else { Ko "meta viewport assente" }
}

$check = @($dest)
if ($SitoUrl) { $check = @($SitoUrl) + $check }
foreach ($u in $check) {
  try {
    $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 20 -MaximumRedirection 5 -UserAgent "Mozilla/5.0 (verifica GPSR IN SHOES)"
    if ($r.StatusCode -eq 200) { Ok "raggiungibile (200): $u" } else { Ko "risposta $($r.StatusCode): $u" }
  } catch {
    $code = 0
    if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
    # 429 = il server risponde ma limita le richieste ravvicinate: riprovare dopo qualche minuto.
    if ($code -eq 429) { Write-Host "[AVVISO] 429 troppe richieste (server attivo, riprovare piu' tardi): $u" -ForegroundColor Yellow }
    else { Ko "non raggiungibile: $u ($($_.Exception.Message))" }
  }
}

if ($fail -eq 0) { Write-Host "`nESITO: OK" -ForegroundColor Green; exit 0 }
Write-Host "`nESITO: $fail problemi" -ForegroundColor Red; exit 1
