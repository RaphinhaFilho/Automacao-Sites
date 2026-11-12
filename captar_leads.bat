@echo off
chcp 65001 > nul
title Captador Nacional de Leads - Revisao

echo ============================================================
echo  INICIANDO CAPTACAO DE LEADS REAIS (COM WHATSAPP / SEM SITE)
echo ============================================================
echo.

python captar_leads.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Ocorreu um problema durante a captacao.
    pause
    exit /b %errorlevel%
)

echo.
echo ============================================================
echo  CAPTACAO CONCLUIDA! ABRINDO 'clientes.json' PARA REVISAO...
echo ============================================================

start "" "clientes.json"

pause