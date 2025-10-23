@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo    SYNVIA PLATFORM - STATUS EM TEMPO REAL
echo ==========================================
echo.

if not exist "ai_module" (
    echo [ERRO] Execute este script a partir do diretório raiz do projeto.
    exit /b 1
)

echo [INFO] Data/Hora: %date% %time%
echo.
echo ==========================================
echo           STATUS DAS PORTAS
echo ==========================================

set /a total_services=0
set /a active_services=0

for %%s in (3000:Frontend:http://localhost:3000 8080:Backend:http://localhost:8080 5001:AI-Service:http://localhost:5001) do (
    set /a total_services+=1
    for /f "tokens=1,2,3 delims=:" %%a in ("%%s") do (
        netstat -an | findstr ":%%a" >nul
        if !errorlevel!==0 (
            echo   %%b ATIVO na porta %%a - %%c
            set /a active_services+=1
        ) else (
            echo   %%b INATIVO na porta %%a
        )
    )
)

echo.
echo ==========================================
echo         TESTES DE CONECTIVIDADE
echo ==========================================

echo [TEST] Frontend...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 3 -UseBasicParsing; Write-Host '   Frontend OK (HTTP' $r.StatusCode')' } catch { Write-Host '   Frontend inacessível' }" 2>nul

echo [TEST] Backend...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8080/actuator/health' -TimeoutSec 3 -UseBasicParsing; Write-Host '   Backend OK (HTTP' $r.StatusCode')' } catch { Write-Host '   Backend inacessível' }" 2>nul

echo [TEST] AI Service...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:5001/health' -TimeoutSec 3 -UseBasicParsing; Write-Host '   AI Service OK (HTTP' $r.StatusCode')' } catch { Write-Host '   AI Service inacessível' }" 2>nul

echo.
echo ==========================================
echo            RESUMO DO SISTEMA
echo ==========================================

set /a percentage=!active_services!*100/!total_services!

if !active_services!==!total_services! (
    echo STATUS: ONLINE (^!percentage!%%^)
    echo ACAO: Sistema pronto para uso
    echo ACESSO: http://localhost:3000
    echo LOGIN: admin@synvia.io / admin123
) else if !active_services! gtr 0 (
    echo STATUS: PARCIAL (^!percentage!%%^)
    echo ACAO: Verificar serviços inativos
    echo DICA: Execute start_system.bat
) else (
    echo STATUS: OFFLINE (^!percentage!%%^)
    echo ACAO: Inicializar sistema
    echo DICA: Execute start_system.bat
)

echo.
echo ==========================================
echo             COMANDOS UTEIS
echo ==========================================
echo Iniciar sistema:     start_system.bat
echo Parar sistema:       stop_system.bat
echo Teste funcional:     test_sistema_seguranca.bat
echo Documentacao:        CENTRAL_DOCUMENTACAO.md
echo Problemas:           SOLUCAO_PROBLEMAS.md
echo.
pause
