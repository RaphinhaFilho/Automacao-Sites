@echo off
chcp 65001 > nul
title Pipeline Automatica - Captacao e Geracao de Landing Pages

if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado! Crie um arquivo .env com GEMINI_API_KEY=sua_chave
    pause
    exit /b 1
)

for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    if "%%a"=="GEMINI_API_KEY" set "GEMINI_API_KEY=%%b"
)

echo ============================================================
echo  ETAPA 1: CAPTANDO E FILTRANDO LEADS REAIS NO BRASIL
echo ============================================================
python captar_leads.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha na etapa de captacao de leads.
    pause
    exit /b %errorlevel%
)

echo.
echo ============================================================
echo  ETAPA 2: GERANDO LANDING PAGES EM LOTE VIA GEMINI
echo ============================================================
python gerar_lote.py

echo.
echo ============================================================
echo  PIPELINE FINALIZADA! TODOS OS SITES ESTAO PRONTOS.
echo ============================================================
pause