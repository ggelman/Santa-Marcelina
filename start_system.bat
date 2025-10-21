@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo    🚀 PADARIA SANTA MARCELINA 
echo    ⚡ INICIALIZACAO ULTRA RAPIDA
echo ==========================================
echo.

REM Verificar se está no diretório correto
if not exist "ai_module" (
    echo ❌ ERRO: Execute este script na pasta SRC
    echo 💡 Caminho correto: C:\projects\FIAP\Fase6\SRC
    pause
    exit /b 1
)

echo [INFO] Parando processos existentes...
for %%p in (3000 5443 8443) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%p') do (
        taskkill /f /pid %%a >nul 2>&1
    )
)

echo [INFO] Aguardando liberacao das portas...
timeout /t 2 /nobreak >nul

echo.
echo ==========================================
echo           🚀 INICIANDO SERVICOS
echo ==========================================

echo [1/3] 🤖 AI Service (Python) - Porta 5443...
start "🤖 AI Service" cmd /k "cd /d %~dp0ai_module && echo [AI] Iniciando... && python ai_service.py"
timeout /t 5 /nobreak >nul

echo [2/3] ⚙️ Backend (Spring) - Porta 8443...
start "⚙️ Backend API" cmd /k "cd /d %~dp0padariaApi && echo [API] Iniciando... && mvn spring-boot:run \"-Dspring.profiles.active=https\""
timeout /t 10 /nobreak >nul

echo [3/3] 🌐 Frontend (React) - Porta 3000...
start "🌐 Frontend Web" cmd /k "cd /d %~dp0FrontGoDgital && echo [WEB] Iniciando... && npm start"

echo.
echo ==========================================
echo        ⏳ AGUARDANDO INICIALIZACAO
echo ==========================================

echo Aguardando servicos ficarem online...
set /a countdown=15
:wait_loop
if !countdown! gtr 0 (
    echo Aguardando: !countdown!s restantes...
    timeout /t 1 /nobreak >nul
    set /a countdown-=1
    goto wait_loop
)

echo.
echo ==========================================
echo         ✅ VERIFICACAO DE STATUS
echo ==========================================

set /a services_ok=0

echo [CHECK] Verificando portas ativas...
for %%p in (3000:Frontend 8443:Backend 5443:AI-Service) do (
    for /f "tokens=1,2 delims=:" %%a in ("%%p") do (
        netstat -an | findstr ":%%a" >nul
        if !errorlevel!==0 (
            echo   ✅ %%b ativo na porta %%a
            set /a services_ok+=1
        ) else (
            echo   ❌ %%b NAO encontrado na porta %%a
        )
    )
)

echo.
if !services_ok!==3 (
    echo ==========================================
    echo            🎉 SISTEMA PRONTO!
    echo ==========================================
    echo.
    echo 🌐 ACESSO PRINCIPAL: http://localhost:3000
    echo 🔐 LOGIN: admin@padaria.com / admin123
    echo.
    echo 📊 APIs Disponiveis:
    echo   • Backend: https://localhost:8443/api
    echo   • AI Service: https://localhost:5443/api/ai  
    echo   • Swagger: https://localhost:8443/swagger-ui.html
    echo.
    echo ⚠️  IMPORTANTE:
    echo   • Aceite certificados SSL quando solicitado
    echo   • Menu "Monitor de Seguranca" apenas para ADMIN
    echo   • Status nao deve mostrar "Desconhecido"
    echo.
    echo 🚀 Abrindo sistema no navegador...
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
) else (
    echo ==========================================
    echo            ⚠️ PROBLEMA DETECTADO
    echo ==========================================
    echo.
    echo Apenas !services_ok!/3 servicos iniciaram corretamente.
    echo.
    echo 🔧 SOLUCOES:
    echo 1. Aguarde mais 1-2 minutos
    echo 2. Verifique logs nos terminais abertos
    echo 3. Execute: check_services_status.bat
    echo 4. Se persistir: stop_all_services.bat e tente novamente
)

echo.
echo ==========================================
pause