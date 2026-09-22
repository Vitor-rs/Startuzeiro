@echo off
chcp 65001 >nul
title Startuzeiro Hub - Painel Centralizado

echo ===================================================================
echo 🚀 Iniciando o Startuzeiro Hub - Painel Central de Ferramentas
echo ===================================================================
echo.

:: Inicia o servidor Python com uv em uma nova janela minimizada
start /min "Startuzeiro Server" uv run scripts/app_server.py

:: Aguarda 2 segundos para o servidor subir
timeout /t 2 /nobreak >nul

:: Abre o navegador padrão na porta 5050
echo 🌐 Abrindo painel no navegador: http://localhost:5050
start http://localhost:5050

echo.
echo [OK] O Startuzeiro Hub está ativo!
echo Para encerrar o servidor, feche a janela do terminal 'Startuzeiro Server' ou pressione Ctrl+C.
echo.
pause
