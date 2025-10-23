@echo off
setlocal enabledelayedexpansion
goto :main

:sleep
powershell -NoLogo -NoProfile -Command "Start-Sleep -Seconds %~1" >nul
exit /b 0

:ensure_db_credentials
set "env_loaded="

if exist "%~dp0synvia-core\.env" (
    for /f "usebackq tokens=1,* delims==" %%a in ("%~dp0synvia-core\.env") do (
        set "key=%%~a"
        set "value=%%~b"
        if defined key if not "!key:~0,1!"=="#" (
            set "key=!key: =!"
            if /i "!key!"=="DB_USERNAME" if not defined DB_USERNAME (
                set "value=!value:"=!"
                set "value=!value:'=!"
                set "DB_USERNAME=!value!"
                set "env_loaded=1"
            )
            if /i "!key!"=="DB_PASSWORD" if not defined DB_PASSWORD (
                set "value=!value:"=!"
                set "value=!value:'=!"
                set "DB_PASSWORD=!value!"
                set "env_loaded=1"
            )
        )
    )
    if defined env_loaded (
        echo [INFO] Variaveis DB carregadas de synvia-core\.env.
    )
)

if not defined DB_USERNAME (
    set "DB_USERNAME=root"
)

if not defined DB_PASSWORD (
    echo [WARN] A variavel DB_PASSWORD nao esta definida.
    echo        Informe a senha MySQL para o usuario !DB_USERNAME! (enter para manter vazio).
    for /f "usebackq delims=" %%p in (`
        powershell -NoLogo -NoProfile -Command ^
            "$secure = Read-Host 'Senha do MySQL (!DB_USERNAME!)' -AsSecureString; ^
             $bstr=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure); ^
             try {[System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)} ^
             finally {[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)}"
    `) do (
        set "DB_PASSWORD=%%p"
    )
)

if not defined DB_PASSWORD (
    echo [WARN] Continuando com senha vazia. Caso o MySQL rejeite a conexao, defina DB_PASSWORD e execute novamente.
) else (
    echo [INFO] Credenciais MySQL prontas para uso.
)

exit /b 0

:main
echo.
echo ==========================================
echo    SYNVIA PLATFORM
echo    ORQUESTRACAO ULTRA RAPIDA
echo ==========================================
echo.

if not exist "ai_module" (
    echo [ERRO] Execute este script na pasta raiz do projeto.
    echo Caminho esperado: C:\projects\FIAP\Fase7\Santa-Marcelina
    pause
    exit /b 1
)

call :ensure_db_credentials

echo [INFO] Parando processos existentes em 3000, 8080 e 5001...
for %%p in (3000 8080 5001) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%%p"') do (
        taskkill /f /pid %%a >nul 2^>^&1
    )
)

echo [INFO] Aguardando liberacao das portas...
call :sleep 2

echo.
echo ==========================================
echo           INICIANDO SERVICOS
echo ==========================================

echo [1/3] AI Service (Python) - Porta 5001 (HTTP)...
start "AI Service" cmd /k "cd /d %~dp0ai_module && set USE_HTTPS=false && set DB_USERNAME=!DB_USERNAME! && set DB_PASSWORD=!DB_PASSWORD! && echo [AI] Iniciando em HTTP (5001)... && python ai_service.py"
call :sleep 5

echo [2/3] Backend (Spring) - Porta 8080 (HTTP)...
start "Backend API" cmd /k "cd /d %~dp0synvia-core && set DB_USERNAME=!DB_USERNAME! && set DB_PASSWORD=!DB_PASSWORD! && echo [API] Iniciando em HTTP (8080)... && mvn spring-boot:run"
call :sleep 10

echo [3/3] Frontend (React) - Porta 3000 (HTTP)...
start "Frontend Web" cmd /k "cd /d %~dp0FrontGoDgital && echo [WEB] Iniciando em HTTP (3000)... && npm start"

echo.
echo ==========================================
echo        AGUARDANDO INICIALIZACAO
echo ==========================================

set /a countdown=15
:wait_loop
if !countdown! gtr 0 (
    echo Aguardando: !countdown!s restantes...
    call :sleep 1
    set /a countdown-=1
    goto :wait_loop
)

echo.
echo ==========================================
echo         VERIFICACAO DE STATUS
echo ==========================================

set /a services_ok=0
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
    echo ACESSO PRINCIPAL: http://localhost:3000
    echo LOGIN: admin@synvia.io / admin123
    echo Backend API: http://localhost:8080/api
    echo AI Service:  http://localhost:5001/api/ai
    echo Swagger:     http://localhost:8080/swagger-ui.html
    echo.
    echo Abrindo sistema no navegador...
    call :sleep 2
    start http://localhost:3000
) else (
    echo ==========================================
    echo            PROBLEMA DETECTADO
    echo ==========================================
    echo Apenas !services_ok!/3 servicos iniciaram corretamente.
    echo.
    echo SOLUCOES:
    echo 1. Aguarde mais alguns segundos e revise os terminais abertos
    echo 2. Execute system_status.bat para diagnostico
    echo 3. Execute stop_system.bat e tente novamente
)

echo.
echo ==========================================
pause
exit /b 0
