@echo off
setlocal enabledelayedexpansion
echo.
echo ==========================================
echo    📊 STATUS DO SISTEMA EM TEMPO REAL
echo ==========================================
echo.

REM Verificar diretório
if not exist "ai_module" (
    echo ❌ Execute este script na pasta SRC
    exit /b 1
)

echo [INFO] Analisando sistema...
echo Data/Hora: %date% %time%
echo.

echo ==========================================
echo         🔍 STATUS DAS PORTAS
echo ==========================================

set /a total_services=0
set /a active_services=0

for %%s in (3000:Frontend:http://localhost:3000 8443:Backend:https://localhost:8443 5443:AI-Service:https://localhost:5443) do (
    set /a total_services+=1
    for /f "tokens=1,2,3 delims=:" %%a in ("%%s") do (
        netstat -an | findstr ":%%a" >nul
        if !errorlevel!==0 (
            echo   ✅ %%b ATIVO na porta %%a - %%c
            set /a active_services+=1
        ) else (
            echo   ❌ %%b INATIVO na porta %%a
        )
    )
)

echo.
echo ==========================================
echo         🧪 TESTES DE CONECTIVIDADE
echo ==========================================

echo [TEST] Frontend HTTP...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 3 -UseBasicParsing; Write-Host '   ✅ Frontend OK (HTTP' $r.StatusCode')' } catch { Write-Host '   ❌ Frontend inacessivel' }" 2>nul

echo [TEST] Backend Health...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'https://localhost:8443/actuator/health' -TimeoutSec 3 -UseBasicParsing -SkipCertificateCheck; Write-Host '   ✅ Backend OK (HTTP' $r.StatusCode')' } catch { Write-Host '   ❌ Backend inacessivel' }" 2>nul

echo [TEST] AI Service Health...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'https://localhost:5443/health' -TimeoutSec 3 -UseBasicParsing -SkipCertificateCheck; Write-Host '   ✅ AI Service OK (HTTP' $r.StatusCode')' } catch { Write-Host '   ❌ AI Service inacessivel' }" 2>nul

echo.
echo ==========================================
echo           📋 RESUMO DO SISTEMA
echo ==========================================

set /a percentage=!active_services!*100/!total_services!

if !active_services!==!total_services! (
    echo 🟢 STATUS: SISTEMA OPERACIONAL ^(!percentage!%%^)
    echo 🎯 ACAO: Sistema pronto para uso
    echo 🌐 ACESSO: http://localhost:3000
    echo 🔐 LOGIN: admin@padaria.com / admin123
) else if !active_services! gtr 0 (
    echo 🟡 STATUS: SISTEMA PARCIAL ^(!percentage!%%^)
    echo 🔧 ACAO: Verificar servicos inativos
    echo 💡 DICA: Execute start_system.bat
) else (
    echo 🔴 STATUS: SISTEMA OFFLINE ^(!percentage!%%^)
    echo 🚀 ACAO: Inicializar sistema
    echo 💡 DICA: Execute start_system.bat
)

echo.
echo ==========================================
echo           🛠️ COMANDOS UTEIS
echo ==========================================
echo.
echo 🚀 Iniciar sistema:     start_system.bat
echo 🛑 Parar sistema:       stop_system.bat  
echo ✅ Testar funcional:    test_sistema_seguranca.bat
echo 📚 Documentacao:        CENTRAL_DOCUMENTACAO.md
echo 🔧 Problemas:           SOLUCAO_PROBLEMAS.md

echo.
echo ==========================================
echo         🔄 ATUALIZACAO AUTOMATICA
echo ==========================================
echo.
echo Este status sera atualizado automaticamente...
timeout /t 5 /nobreak >nul

REM Loop de monitoramento (opcional)
choice /t 10 /c YN /d N /m "Continuar monitoramento em tempo real? (Y/N)"
if !errorlevel!==1 (
    cls
    goto :inicio
)

pause