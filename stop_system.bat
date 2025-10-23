@echo off
echo.
echo ==========================================
echo    PARADA RAPIDA DOS SERVICOS SYNVIA
echo ==========================================
echo.

echo [INFO] Finalizando processos nas portas 3000, 8080 e 5001...
set /a stopped=0

for %%p in (3000:Frontend 8080:Backend 5001:AI-Service) do (
    for /f "tokens=1,2 delims=:" %%a in ("%%p") do (
        echo [STOP] Verificando porta %%a (%%b)...
        for /f "tokens=5" %%c in ('netstat -ano 2^>nul ^| findstr ":%%a"') do (
            echo   Encerrando PID %%c...
            taskkill /PID %%c /F >nul 2>&1
            if !errorlevel!==0 set /a stopped+=1
        )
    )
)

echo.
echo [INFO] Aguardando liberacao das portas...
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo          VERIFICACAO FINAL
echo ==========================================

set /a ports_free=0
for %%p in (3000 8080 5001) do (
    netstat -an | findstr ":%%p" >nul 2>&1
    if !errorlevel! neq 0 (
        echo   Porta %%p livre
        set /a ports_free+=1
    ) else (
        echo   Porta %%p ainda ocupada
    )
)

echo.
if !ports_free!==3 (
    echo TODOS OS SERVICOS FORAM ENCERRADOS.
) else (
    echo Ainda existem processos ativos. Feche os terminais abertos, se necessário.
)

echo.
echo ==========================================
pause
