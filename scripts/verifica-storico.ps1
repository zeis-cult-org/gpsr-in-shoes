# Verifica del sito storico lost-95.github.io/cult-milano-gpsr (solo lettura).
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\verifica-storico.ps1 -Fase prima
#       powershell -ExecutionPolicy Bypass -File scripts\verifica-storico.ps1 -Fase dopo
#       aggiungere -Base http://127.0.0.1:8001/cult-milano-gpsr per il test locale
param(
  [ValidateSet("prima","dopo")][string]$Fase = "prima",
  [string]$Base = "https://lost-95.github.io/cult-milano-gpsr"
)
$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$fail = 0
function Ok($m) { Write-Host "[OK]   $m" -ForegroundColor Green }
function Ko($m) { Write-Host "[ERRORE] $m" -ForegroundColor Red; $script:fail++ }

$destinazione = "https://gpsr.in-shoes.it/"
# MD5 della homepage storica originale (commit 432f167 del 30/07/2026)
$md5Originale = "2B4EC01EA01EBBF423AE8EC4416FB6EF"
# SHA-256 dei 10 PDF, dal backup del 04/11/2026: non devono mai cambiare
$pdf = [ordered]@{
  "ballerina.pdf"        = "CDD1553DD6C8BD664A78752DCDB1CF60579C2978970665C02A617C29930B56FB"
  "mocassino.pdf"        = "17F9DA28315C688FF6E4688D5F7480A429CD9B4E379BFCF7930EF19ACE75BF62"
  "mule.pdf"             = "61DE5A643E8DB5C6DFA858AE738E56B0D053235F340B8EAE27F834BA9B8AE20E"
  "sandalo.pdf"          = "35B20A4BBFCD507435E8BF7E7098F00337E761B6885F08A89356267C76E4DBA4"
  "scarpa_con_tacco.pdf" = "0058CA0F41D9789D9FD3C4F8013ADC80EE82B34A8582A2F9976936334017D258"
  "slides.pdf"           = "106C56A1C0CFEEC017A5D9E8EFC8C1FC85EB69F01E70EC2CB59EE34CAB69C040"
  "sneaker.pdf"          = "1C0875857FFCD3F2BC006335BE4541D5B7F525F24A86E1857781EBAFDB0447C0"
  "stivale.pdf"          = "8BCB43B3427779821D2AE5E0678EF0604DBD323087B77606D354E2B37D5C70CA"
  "stivaletto.pdf"       = "FA45074B2395E95A0719E215B03DC1DAD3F3F2FC916A21A0F514BD5EDE5AD971"
  "stringata.pdf"        = "536715ECF2AAB92923B22D2567C9425FF822E8DDF940EAB70FFDA85283FB454B"
}
$tmp = Join-Path $env:TEMP "verifica-storico.bin"

function Scarica($url) {
  $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30 -OutFile $tmp -PassThru -UserAgent "Mozilla/5.0 (verifica GPSR)"
  return $r.StatusCode
}

Write-Host "Fase: $Fase   Base: $Base`n"

foreach ($p in @("/", "/index.html", "/?src=qr")) {
  $u = "$Base$p"
  try {
    $code = Scarica $u
    $md5 = (Get-FileHash $tmp -Algorithm MD5).Hash
    $html = [IO.File]::ReadAllText($tmp, [Text.Encoding]::UTF8)
    if ($code -ne 200) { Ko "$u risponde $code"; continue }
    if ($Fase -eq "prima") {
      if ($md5 -eq $md5Originale) { Ok "$u : homepage originale (MD5 invariato)" } else { Ko "$u : homepage diversa dall'originale (MD5 $md5)" }
    } else {
      $meta = $html -match [regex]::Escape('http-equiv="refresh" content="0; url=' + $destinazione + '"')
      $js   = $html.Contains('location.replace("' + $destinazione + '")')
      $link = $html.Contains('href="' + $destinazione + '"')
      if ($meta -and $js -and $link) { Ok "$u : redirect verso $destinazione (meta refresh + script + link)" }
      else { Ko "$u : redirect incompleto (meta=$meta script=$js link=$link)" }
    }
  } catch { Ko "$u non raggiungibile ($($_.Exception.Message))" }
}

foreach ($f in $pdf.Keys) {
  $u = "$Base/$f"
  try {
    $code = Scarica $u
    $h = (Get-FileHash $tmp -Algorithm SHA256).Hash
    if ($code -eq 200 -and $h -eq $pdf[$f]) { Ok "$f : 200, contenuto invariato" } else { Ko "$f : codice $code, SHA-256 $h" }
  } catch { Ko "$f non raggiungibile ($($_.Exception.Message))" }
}

if ($Fase -eq "dopo") {
  try {
    $code = Scarica $destinazione
    if ($code -eq 200) { Ok "destinazione $destinazione : 200" } else { Ko "destinazione $destinazione : $code" }
  } catch { Ko "destinazione non raggiungibile ($($_.Exception.Message))" }
}

if ([IO.File]::Exists($tmp)) { [IO.File]::Delete($tmp) }
if ($fail -eq 0) { Write-Host "`nESITO: OK" -ForegroundColor Green; exit 0 }
Write-Host "`nESITO: $fail problemi" -ForegroundColor Red; exit 1
