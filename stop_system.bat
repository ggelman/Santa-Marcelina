@echo off
echo.
echo ==========================================
echo    🛑 PARADA RAPIDA DE SERVICOS
echo ==========================================
echo.

echo [INFO] Finalizando processos nas portas...
set /a stopped=0

for %%p in (3000:Frontend 8443:Backend 5443:AI-Service) do (
    for /f "tokens=1,2 delims=:" %%a in ("%%p") do (
        echo [STOP] Verificando porta %%a (%%b)...
        for /f "tokens=5" %%c in ('netstat -ano 2^>nul ^| findstr ":%%a"') do (
            echo   🛑 Parando PID %%c...
            taskkill /PID %%c /F >nul 2>&1
            if !errorlevel!==0 set /a stopped+=1
        )
    )
)

echo.
echo [INFO] Aguardando liberacao completa...
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo          ✅ VERIFICACAO FINAL
echo ==========================================

set /a ports_free=0
for %%p in (3000 8443 5443) do (
    netstat -an | findstr ":%%p" >nul 2>&1
    if !errorlevel! neq 0 (
        echo   ✅ Porta %%p livre
        set /a ports_free+=1
    ) else (
        echo   ⚠️  Porta %%p ainda ocupada
    )
)

echo.
if !ports_free!==3 (
    echo 🎉 TODOS OS SERVICOS PARADOS COM SUCESSO!
    echo Sistema limpo para reinicializacao.
) else (
    echo ⚠️  Alguns processos podem ainda estar ativos.
    echo Feche manualmente os terminais se necessario.
)

echo.
echo ==========================================
pause