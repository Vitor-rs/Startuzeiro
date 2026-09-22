@echo off
title Changedetection.io - Startuzeiro Monitor
echo ========================================================
echo   Iniciando Changedetection.io (Monitoramento de Sites)
echo   Painel Web: http://localhost:5005
echo ========================================================
echo.

if not exist dados\changedetection_data mkdir dados\changedetection_data

uv run changedetection.io -p 5005 -d dados\changedetection_data
pause
