@echo off
echo ==========================================
echo    TESTE AUTOMATIZADO - SYNVIA PLATFORM
echo ==========================================
echo.

echo [INFO] Verificando serviços ativos (HTTP)...
echo.

REM Frontend
echo [1/3] Frontend (porta 3000)...
netstat -an | findstr ":3000" >nul
if %errorlevel%==0 (
    echo   OK: Frontend ativo em http://localhost:3000
) else (
    echo   FALHA: Frontend nao encontrado
    echo   Ação: cd FrontGoDgital && npm start
)
echo.

REM Backend
echo [2/3] Backend (porta 8080)...
netstat -an | findstr ":8080" >nul
if %errorlevel%==0 (
    echo   OK: Backend ativo em http://localhost:8080
) else (
    echo   FALHA: Backend nao encontrado
    echo   Ação: cd synvia-core && mvn spring-boot:run
)
echo.

REM AI Service
echo [3/3] AI Service (porta 5001)...
netstat -an | findstr ":5001" >nul
if %errorlevel%==0 (
    echo   OK: AI Service ativo em http://localhost:5001
) else (
    echo   FALHA: AI Service nao encontrado
    echo   Ação: cd ai_module && set USE_HTTPS=false && python ai_service.py
)
echo.

echo ==========================================
echo         TESTES DE CONECTIVIDADE
echo ==========================================
echo.

echo [TESTE] Frontend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 5 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   Frontend OK (HTTP 200)' } else { Write-Host '   Frontend respondeu com status:' $response.StatusCode } } catch { Write-Host '   Frontend inacessível' }"
echo.

echo [TESTE] Backend /actuator/health...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080/actuator/health' -TimeoutSec 5 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   Backend OK (HTTP 200)' } else { Write-Host '   Backend respondeu com status:' $response.StatusCode } } catch { Write-Host '   Backend inacessível' }"
echo.

echo [TESTE] AI Service /health...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5001/health' -TimeoutSec 5 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   AI Service OK (HTTP 200)' } else { Write-Host '   AI Service respondeu com status:' $response.StatusCode } } catch { Write-Host '   AI Service inacessível' }"
echo.

echo ==========================================
echo             RESUMO
echo ==========================================
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8080/api
echo AI Service:http://localhost:5001/api/ai
echo Login:     admin@synvia.io / admin123
echo.
pause
