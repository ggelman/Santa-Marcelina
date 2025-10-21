@echo off
echo ==========================================
echo    SCRIPT DE TESTE AUTOMATIZADO
echo    Sistema Monitor de Seguranca
echo ==========================================
echo.

echo [INFO] Verificando servicos ativos...
echo.

REM Verificar Frontend
echo [1/3] Testando Frontend (porta 3000)...
netstat -an | findstr ":3000" >nul
if %errorlevel%==0 (
    echo   ✅ Frontend ATIVO em http://localhost:3000
) else (
    echo   ❌ Frontend NAO ENCONTRADO
    echo   💡 Execute: cd FrontGoDgital ^&^& npm start
)
echo.

REM Verificar Backend
echo [2/3] Testando Backend (porta 8443)...
netstat -an | findstr ":8443" >nul
if %errorlevel%==0 (
    echo   ✅ Backend ATIVO em https://localhost:8443
) else (
    echo   ❌ Backend NAO ENCONTRADO
    echo   💡 Execute: cd padariaApi ^&^& mvn spring-boot:run "-Dspring.profiles.active=https"
)
echo.

REM Verificar AI Service
echo [3/3] Testando AI Service (porta 5443)...
netstat -an | findstr ":5443" >nul
if %errorlevel%==0 (
    echo   ✅ AI Service ATIVO em https://localhost:5443
) else (
    echo   ❌ AI Service NAO ENCONTRADO
    echo   💡 Execute: cd ai_module ^&^& python ai_service.py
)
echo.

echo ==========================================
echo           TESTES DE CONECTIVIDADE
echo ==========================================
echo.

REM Teste básico do Frontend
echo [TESTE] Conectividade Frontend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 5 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   ✅ Frontend respondendo (HTTP 200)' } else { Write-Host '   ⚠️  Frontend respondeu com status:' $response.StatusCode } } catch { Write-Host '   ❌ Frontend nao acessivel' }"
echo.

REM Teste básico do Backend
echo [TESTE] Conectividade Backend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://localhost:8443/actuator/health' -TimeoutSec 5 -UseBasicParsing -SkipCertificateCheck; if($response.StatusCode -eq 200) { Write-Host '   ✅ Backend respondendo (HTTP 200)' } else { Write-Host '   ⚠️  Backend respondeu com status:' $response.StatusCode } } catch { Write-Host '   ❌ Backend nao acessivel' }"
echo.

REM Teste básico do AI Service
echo [TESTE] Conectividade AI Service...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://localhost:5443/health' -TimeoutSec 5 -UseBasicParsing -SkipCertificateCheck; if($response.StatusCode -eq 200) { Write-Host '   ✅ AI Service respondendo (HTTP 200)' } else { Write-Host '   ⚠️  AI Service respondeu com status:' $response.StatusCode } } catch { Write-Host '   ❌ AI Service nao acessivel' }"
echo.

echo ==========================================
echo              TESTES DE API
echo ==========================================
echo.

echo [API] Testando endpoints de seguranca...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://localhost:8443/api/ai/security/health' -TimeoutSec 5 -UseBasicParsing -SkipCertificateCheck; if($response.StatusCode -eq 200) { Write-Host '   ✅ Endpoint /api/ai/security/health OK' } else { Write-Host '   ⚠️  Endpoint health status:' $response.StatusCode } } catch { Write-Host '   ❌ Endpoint /api/ai/security/health FALHOU' }"

powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://localhost:8443/api/ai/security/stats' -TimeoutSec 5 -UseBasicParsing -SkipCertificateCheck; if($response.StatusCode -eq 401) { Write-Host '   ✅ Endpoint /api/ai/security/stats protegido (401 - OK)' } elseif($response.StatusCode -eq 200) { Write-Host '   ✅ Endpoint /api/ai/security/stats acessivel' } else { Write-Host '   ⚠️  Endpoint stats status:' $response.StatusCode } } catch { Write-Host '   ❌ Endpoint /api/ai/security/stats FALHOU' }"
echo.

echo ==========================================
echo            RELATORIO FINAL
echo ==========================================
echo.

echo 📋 CHECKLIST DE VALIDACAO:
echo.
echo [ ] Frontend acessivel em http://localhost:3000
echo [ ] Backend acessivel em https://localhost:8443  
echo [ ] AI Service acessivel em https://localhost:5443
echo [ ] Endpoints de seguranca respondendo
echo [ ] Login funcionando (admin@padaria.com / admin123)
echo [ ] Monitor de Seguranca acessivel no menu
echo [ ] Abas funcionando (Dashboard, Alertas, Configuracoes)
echo [ ] Metricas carregando
echo [ ] Design consistente com plataforma
echo.

echo 🚀 PROXIMOS PASSOS:
echo 1. Abrir navegador em http://localhost:3000
echo 2. Fazer login com admin@padaria.com / admin123
echo 3. Navegar para Monitor de Seguranca
echo 4. Testar todas as funcionalidades manualmente
echo 5. Verificar responsividade
echo.

echo ⚠️  IMPORTANTE:
echo - Aceite os certificados SSL quando solicitado
echo - Verifique console do navegador para erros
echo - Teste em diferentes resolucoes
echo.

echo ==========================================
echo          TESTE CONCLUIDO
echo ==========================================
pause