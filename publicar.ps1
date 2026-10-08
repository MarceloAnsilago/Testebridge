$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
git -c http.sslBackend=openssl push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'Falha no envio. Conclua o login do GitHub no seu Windows e repita.' }
