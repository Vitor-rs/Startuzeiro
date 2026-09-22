# Setup e Verificação de Ambiente para o Startuzeiro
# Pode ser executado em qualquer máquina Windows (Desktop ou Laptop)
# Executar: powershell -ExecutionPolicy Bypass -File scripts/setup/setup_machine.ps1

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "[*] STARTUZEIRO - Sincronizacao & Setup da Maquina" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

$RepoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Write-Host "Diretorio do Repositorio: $RepoRoot" -ForegroundColor Gray
Write-Host "Usuario do Windows: $env:USERNAME" -ForegroundColor Gray
Write-Host "Computador: $env:COMPUTERNAME" -ForegroundColor Gray

# 1. Verificar e criar .env
Write-Host "`n[1/4] Verificando arquivo .env..." -ForegroundColor Yellow
$EnvPath = Join-Path $RepoRoot ".env"
$EnvExamplePath = Join-Path $RepoRoot ".env.example"

if (-not (Test-Path $EnvPath)) {
    if (Test-Path $EnvExamplePath) {
        Copy-Item $EnvExamplePath $EnvPath
        Write-Host "   [OK] Arquivo .env criado a partir de .env.example!" -ForegroundColor Green
        Write-Host "   [!] Lembre-se de preencher suas chaves reais no arquivo .env" -ForegroundColor Yellow
    } else {
        Write-Host "   [ERRO] .env.example nao encontrado para copiar!" -ForegroundColor Red
    }
} else {
    Write-Host "   [OK] Arquivo .env ja existe e esta pronto." -ForegroundColor Green
}

# Carregar variáveis do .env dinamicamente
$envVars = @{}
if (Test-Path $EnvPath) {
    Get-Content $EnvPath | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $parts = $line.Split("=", 2)
            $varName = $parts[0].Trim()
            $varValue = $parts[1].Trim()
            $envVars[$varName] = $varValue
        }
    }
}

# 2. Verificar uv
Write-Host "`n[2/4] Verificando uv (Astral Python Package Manager)..." -ForegroundColor Yellow
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if ($null -eq $uvCmd) {
    Write-Host "   [!] uv nao encontrado no PATH!" -ForegroundColor Yellow
    Write-Host "   Instalando uv automaticamente via script oficial da Astral..." -ForegroundColor Cyan
    try {
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
        Write-Host "   [OK] uv instalado com sucesso!" -ForegroundColor Green
    } catch {
        Write-Host "   [ERRO] Falha ao instalar uv automaticamente. Execute manualmente: irm https://astral.sh/uv/install.ps1 | iex" -ForegroundColor Red
    }
} else {
    $uvVer = uv --version
    Write-Host "   [OK] $uvVer encontrado em: $($uvCmd.Source)" -ForegroundColor Green
}

# 3. Verificar Node.js e npx (necessario para MCPs)
Write-Host "`n[3/4] Verificando Node.js e npx..." -ForegroundColor Yellow
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
$npxCmd = Get-Command npx -ErrorAction SilentlyContinue

if ($null -eq $nodeCmd -or $null -eq $npxCmd) {
    Write-Host "   [!] Node.js / npx nao encontrado. E recomendado instalar Node.js para rodar os MCPs via npx." -ForegroundColor Yellow
} else {
    $nodeVer = node -v
    Write-Host "   [OK] Node.js ($nodeVer) e npx encontrados!" -ForegroundColor Green
}

# 4. Configuracao dos MCPs no Antigravity / Gemini (~/.gemini/config/mcp_config.json)
Write-Host "`n[4/4] Verificando configuracao global dos MCPs do Antigravity..." -ForegroundColor Yellow
$GeminiConfigDir = Join-Path $env:USERPROFILE ".gemini\config"
$McpConfigFile = Join-Path $GeminiConfigDir "mcp_config.json"

if (-not (Test-Path $GeminiConfigDir)) {
    New-Item -ItemType Directory -Path $GeminiConfigDir -Force | Out-Null
}

$mcpData = @{ "mcpServers" = @{} }
if (Test-Path $McpConfigFile) {
    try {
        $rawJson = Get-Content -Path $McpConfigFile -Raw -Encoding UTF8
        $mcpData = $rawJson | ConvertFrom-Json
    } catch {
        Write-Host "   [!] Erro ao ler $McpConfigFile existente." -ForegroundColor Yellow
    }
}

# Garantir estrutura
if (-not $mcpData.mcpServers) {
    $mcpData | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value (New-Object PSObject) -Force
}

$modified = $false

# Obter chaves do .env
$transcriptKey = if ($envVars["TRANSCRIPT_API_KEY"]) { $envVars["TRANSCRIPT_API_KEY"] } else { "SUA_CHAVE_TRANSCRIPT_AQUI" }
$firecrawlKey = if ($envVars["FIRECRAWL_API_KEY"]) { $envVars["FIRECRAWL_API_KEY"] } else { "SUA_CHAVE_FIRECRAWL_AQUI" }
$context7Key = if ($envVars["CONTEXT7_API_KEY"]) { $envVars["CONTEXT7_API_KEY"] } else { "SUA_CHAVE_CONTEXT7_AQUI" }

# Configurar transcript-api se nao existir
if (-not $mcpData.mcpServers."transcript-api") {
    $transcriptObj = [PSCustomObject]@{
        serverUrl = "https://transcriptapi.com/mcp"
        headers = [PSCustomObject]@{
            Authorization = "Bearer $transcriptKey"
        }
    }
    $mcpData.mcpServers | Add-Member -MemberType NoteProperty -Name "transcript-api" -Value $transcriptObj -Force
    $modified = $true
    Write-Host "   [+] MCP 'transcript-api' adicionado ao mcp_config.json!" -ForegroundColor Green
} else {
    Write-Host "   [OK] MCP 'transcript-api' ja configurado." -ForegroundColor Green
}

# Configurar firecrawl se nao existir
if (-not $mcpData.mcpServers."firecrawl") {
    $firecrawlObj = [PSCustomObject]@{
        command = "npx"
        args = @("-y", "firecrawl-mcp")
        env = [PSCustomObject]@{
            FIRECRAWL_API_KEY = "$firecrawlKey"
        }
    }
    $mcpData.mcpServers | Add-Member -MemberType NoteProperty -Name "firecrawl" -Value $firecrawlObj -Force
    $modified = $true
    Write-Host "   [+] MCP 'firecrawl' adicionado ao mcp_config.json!" -ForegroundColor Green
} else {
    Write-Host "   [OK] MCP 'firecrawl' ja configurado." -ForegroundColor Green
}

# Configurar context7 se nao existir
if (-not $mcpData.mcpServers."context7") {
    $context7Obj = [PSCustomObject]@{
        serverUrl = "https://mcp.context7.com/mcp"
        headers = [PSCustomObject]@{
            Authorization = "Bearer $context7Key"
        }
    }
    $mcpData.mcpServers | Add-Member -MemberType NoteProperty -Name "context7" -Value $context7Obj -Force
    $modified = $true
    Write-Host "   [+] MCP 'context7' adicionado ao mcp_config.json!" -ForegroundColor Green
} else {
    Write-Host "   [OK] MCP 'context7' ja configurado." -ForegroundColor Green
}

if ($modified) {
    $newJson = $mcpData | ConvertTo-Json -Depth 10
    Set-Content -Path $McpConfigFile -Value $newJson -Encoding UTF8
    Write-Host "   [OK] $McpConfigFile atualizado com sucesso!" -ForegroundColor Green
}

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "Setup finalizado! Seu ambiente esta 100% pronto." -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""
