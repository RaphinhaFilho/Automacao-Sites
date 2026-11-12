@echo off
chcp 65001 > nul

if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado! Crie um arquivo .env com GEMINI_API_KEY=sua_chave
    pause
    exit /b 1
)

for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    if "%%a"=="GEMINI_API_KEY" set "GEMINI_API_KEY=%%b"
)

python gerar_lote.py
pause