@echo off
chcp 65001 > nul
set NOME_PROJETO=%1

if "%NOME_PROJETO%"=="" (
    echo ⚠️ Erro: Forneca o nome do projeto.
    echo Exemplo: .\novo-cliente.bat barbearia-dom-pedro
    exit /b 1
)

echo.
echo ===================================================
echo 🚀 Criando estrutura automatizada para: %NOME_PROJETO%
echo ===================================================
echo.

:: 1. Clona o modelo base do GitHub para a nova pasta do cliente em Landing-Pages
git clone https://github.com/RaphinhaFilho/template-landing-page.git %NOME_PROJETO%

:: 2. Entra na pasta do novo cliente
cd %NOME_PROJETO%

:: 3. Limpa o Git antigo para isolar o historico do cliente
rmdir /s /q .git
git init

:: 4. Instala as dependencias
echo 📦 Instalando dependencias...
call npm install

:: Copia o arquivo .env da pasta base para a pasta do cliente
copy /y ..\template-landing-page\.env .env > nul

echo.
echo 🎨 Escolha o estilo visual do cliente:
echo [1] Clean (templates-design/design-clean.md)
echo [2] Dark  (templates-design/design-dark.md)
echo [3] Warm  (templates-design/design-warm.md)
set /p OPCAO_ESTILO="Digite o numero (1, 2 ou 3): "

if "%OPCAO_ESTILO%"=="1" copy /y templates-design\design-clean.md DESIGN.md > nul
if "%OPCAO_ESTILO%"=="2" copy /y templates-design\design-dark.md DESIGN.md > nul
if "%OPCAO_ESTILO%"=="3" copy /y templates-design\design-warm.md DESIGN.md > nul

echo.
echo 📝 Cole o prompt exclusivo do cliente abaixo e pressione ENTER:
set /p PROMPT_CLIENTE="Prompt: "

echo.
echo ⚡ Gerando a Landing Page via API...
node generate.js "%PROMPT_CLIENTE%"

echo.
echo ✨ Projeto pronto e index.html gerado! Abrindo no VS Code...
code "%CD%"