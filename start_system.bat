@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo    SYNVIA PLATFORM
echo    ORQUESTRACAO ULTRA RAPIDA
echo ==========================================
echo.

REM Verificar se esta no diretorio correto
if not exist "ai_module" (
    echo [ERRO] Execute este script na pasta SRC
    echo Caminho correto: C:\projects\FIAP\
    pause
    exit /b 1
)

echo [INFO] Parando processos existentes em 3000, 8080 e 5001...
for %%p in (3000 8080 5001) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%p') do (
        taskkill /f /pid %%a >nul 2>&1
    )
)

echo [INFO] Aguardando liberacao das portas...
timeout /t 2 /nobreak >nul

echo.
echo ==========================================
echo           INICIANDO SERVICOS
echo ==========================================

echo [1/3] AI Service (Python) - Porta 5001 (HTTP)...
start "AI Service" cmd /k "cd /d %~dp0ai_module && set USE_HTTPS=false && echo [AI] Iniciando em HTTP... && python ai_service.py"
timeout /t 5 /nobreak >nul

echo [2/3] Backend (Spring) - Porta 8080 (HTTP)...
start "Backend API" cmd /k "cd /d %~dp0synvia-core && echo [API] Iniciando em HTTP... && mvn spring-boot:run"
timeout /t 10 /nobreak >nul

echo [3/3] Frontend (React) - Porta 3000 (HTTP)...
start "Frontend Web" cmd /k "cd /d %~dp0FrontGoDgital && echo [WEB] Iniciando... && npm start"

echo.
echo ==========================================
echo        AGUARDANDO INICIALIZACAO
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
echo         VERIFICACAO DE STATUS
echo ==========================================

set /a services_ok=0

echo [CHECK] Verificando portas ativas...
for %%p in (3000:Frontend 8080:Backend 5001:AI-Service) do (
    for /f "tokens=1,2 delims=:" %%a in ("%%p") do (
        netstat -an | findstr ":%%a" >nul
        if !errorlevel!==0 (
            echo   %%b ativo na porta %%a
            set /a services_ok+=1
        ) else (
            echo   %%b NAO encontrado na porta %%a
        )
    )
)

echo.
if !services_ok!==3 (
    echo ==========================================
    echo            SISTEMA PRONTO!
    echo ==========================================
    echo.
    echo ACESSO PRINCIPAL: http://localhost:3000
    echo LOGIN: admin@synvia.io / admin123
    echo.
    echo APIs Disponiveis:
    echo   Backend: http://localhost:8080/api
    echo   AI Service: http://localhost:5001/api/ai
    echo   Swagger: http://localhost:8080/swagger-ui.html
    echo.
    echo IMPORTANTE:
    echo   Todos os servicos estao em HTTP para desenvolvimento e testes.
    echo   Ajuste variaveis de ambiente para habilitar HTTPS quando necessario.
    echo.
    echo Abrindo sistema no navegador...
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
) else (
    echo ==========================================
    echo            PROBLEMA DETECTADO
    echo ==========================================
    echo.
    echo Apenas !services_ok!/3 servicos iniciaram corretamente.
    echo.
    echo SOLUCOES:
    echo 1. Aguarde mais 1-2 minutos
    echo 2. Verifique logs nos terminais abertos
    echo 3. Execute: system_status.bat
    echo 4. Se persistir: stop_all_services.bat e tente novamente
)

echo.
echo ==========================================
pause
