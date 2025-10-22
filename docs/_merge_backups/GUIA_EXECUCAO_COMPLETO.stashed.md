# ­ƒÜÇ Guia Completo de Execu├º├úo - Sistema HTTPS

## ­ƒôï Pr├®-requisitos

- **Java 17+** instalado
- **Node.js 18+** instalado
- **Python 3.8+** instalado
- **Maven** configurado
- **PowerShell** (Windows)

## ­ƒöº 1. Prepara├º├úo do Ambiente

### 1.1 Verificar Instala├º├Áes
```powershell
java -version
node --version
python --version
mvn --version
```

### 1.2 Instalar Depend├¬ncias Python (AI Module)
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\ai_module
pip install -r requirements.txt
```

### 1.3 Instalar Depend├¬ncias Frontend
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\FrontGoDgital
npm install
```

## ­ƒøí´©Å 2. Certificados SSL

Os certificados SSL j├í est├úo gerados na pasta `ssl_certificates/`:
- `server.crt` - Certificado p├║blico
- `server.key` - Chave privada
- `keystore.p12` - Keystore para Spring Boot

## ­ƒÜÇ 3. Inicializa├º├úo dos Servi├ºos

### 3.1 AI Service (Python Flask) - Porta 5443
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\ai_module
python ai_service.py
```
**Aguarde** at├® ver: `Running on https://0.0.0.0:5443`

### 3.2 Backend (Spring Boot) - Porta 8443
**Em um novo terminal PowerShell:**
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\padariaApi
mvn spring-boot:run "-Dspring.profiles.active=https"
```
**Aguarde** at├® ver: `Started PadariaApiApplication`

### 3.3 Frontend (React) - Porta 3000
**Em um novo terminal PowerShell:**

ÔÜá´©Å **Para notebooks corporativos (RECOMENDADO):**
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\FrontGoDgital
npm start
```
*Inicia a aplica├º├úo React completa em HTTP na porta 3000 (sem certificados)*

**Para computadores pessoais (com HTTPS):**
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\FrontGoDgital
npm run start:https
```
*Inicia a aplica├º├úo React em HTTPS na porta 3443 (requer instala├º├úo de certificado)*

## ­ƒöì 4. Verifica├º├úo dos Servi├ºos

### 4.1 Verificar Portas Ativas
```powershell
netstat -an | findstr ":3443"
netstat -an | findstr ":5443"
netstat -an | findstr ":8443"
```

### 4.2 Testar Conectividade
```powershell
# Testar AI Service
curl -k https://localhost:5443/health

# Testar Backend
curl -k https://localhost:8443/actuator/health
```

## ­ƒîÉ 5. Configura├º├úo do Navegador

### 5.1 Aceitar Certificados SSL
1. **Frontend**: Acesse `https://localhost:3443`
   - Clique em "Avan├ºado" 
   - Clique em "Continuar para localhost (n├úo seguro)"

2. **Backend**: Acesse `https://localhost:8443`
   - Clique em "Avan├ºado"
   - Clique em "Continuar para localhost (n├úo seguro)"

3. **AI Service**: Acesse `https://localhost:5443`
   - Clique em "Avan├ºado"
   - Clique em "Continuar para localhost (n├úo seguro)"

### 5.2 URLs de Acesso

**Para ambiente corporativo (HTTP):**
- **Frontend**: http://localhost:3000
- **Backend API**: https://localhost:8443/api (aceitar certificado)
- **AI Service**: https://localhost:5443/api/ai (aceitar certificado)

**Para ambiente pessoal (HTTPS completo):**
- **Frontend**: https://localhost:3443
- **Backend API**: https://localhost:8443/api
- **AI Service**: https://localhost:5443/api/ai
- **Swagger UI**: https://localhost:8443/swagger-ui.html

## Ô£à 6. Teste da Aplica├º├úo

### 6.1 Teste de Login
**ÔÜá´©Å IMPORTANTE: FA├çA LOGIN PRIMEIRO!**

1. **Acesse a aplica├º├úo React:** `http://localhost:3000`

2. **PRIMEIRO PASSO - LOGIN OBRIGAT├ôRIO:**
   - ­ƒöù Clique em "Login" ou acesse diretamente: `http://localhost:3000/login`
   - **Email:** `admin@padaria.com`
   - **Senha:** `admin123`
   - Ô£à Clique em "Entrar"
   - ­ƒöä Voc├¬ ser├í redirecionado para o dashboard automaticamente

3. **AP├ôS O LOGIN - Sistema Completo Dispon├¡vel:**
   - Ô£à Dashboard completo com dados reais
   - Ô£à Todas as funcionalidades desbloqueadas:
     - ­ƒôè Dashboard & Dashboard Financeiro
     - ­ƒøÆ Cadastro de Produtos & Nova Venda
     - ­ƒæÑ Gerenciamento de Clientes & Usu├írios
     - ­ƒôª Gest├úo de Estoque & Categorias
     - ­ƒôê Relat├│rios & Hist├│rico de Vendas
     - ­ƒñû Chat IA & Previs├úo IA
     - ÔÜÖ´©Å Sistema de Backup

4. **ÔÜá´©Å SEM LOGIN:** 
   - ÔØî Voc├¬ ver├í erros 403 (Forbidden) nas APIs
   - ÔØî Dashboard e relat├│rios n├úo carregar├úo dados
   - ­ƒöä Sistema redirecionar├í automaticamente para login

3. **APIs Backend (quando iniciadas):**
   - Backend: `https://localhost:8443/api`
   - Swagger: `https://localhost:8443/swagger-ui.html`

### 6.2 Teste de API
```powershell
# Teste b├ísico da API
curl -k -X GET https://localhost:8443/api/produtos

# Teste com autentica├º├úo (substitua TOKEN pelo token real)
curl -k -H "Authorization: Bearer TOKEN" https://localhost:8443/api/produtos
```

### 6.3 Teste do AI Service
```powershell
# Teste b├ísico
curl -k -X POST https://localhost:5443/api/ai/chat -H "Content-Type: application/json" -d "{\"message\":\"Ol├í\"}"
```

## ­ƒøá´©Å 7. Scripts de Inicializa├º├úo Autom├ítica

### 7.1 Script para Todos os Servi├ºos
```powershell
# Criar arquivo: start_all_services.bat
@echo off
echo Iniciando todos os servi├ºos HTTPS...

start "AI Service" cmd /k "cd /d C:\projects\FIAP\\ai_module && python ai_service.py"
timeout /t 5 /nobreak > nul

start "Backend" cmd /k "cd /d C:\projects\FIAP\\padariaApi && mvn spring-boot:run \"-Dspring.profiles.active=https\""
timeout /t 10 /nobreak > nul

start "Frontend" cmd /k "cd /d C:\projects\FIAP\\FrontGoDgital && npm start"

echo Todos os servi├ºos foram iniciados!
echo Frontend: https://localhost:3443
echo Backend: https://localhost:8443
echo AI Service: https://localhost:5443
pause
```

### 7.2 Executar Script
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina
.\start_all_services.bat
```

## ­ƒöº 8. Solu├º├úo de Problemas

### 8.1 Portas em Uso
```powershell
# Verificar processos usando as portas
netstat -ano | findstr ":3443"
netstat -ano | findstr ":5443"
netstat -ano | findstr ":8443"

# Finalizar processo (substitua PID pelo ID do processo)
taskkill /PID 1234 /F
```

### 8.2 Problemas de Certificado
- **Erro**: "Sua conex├úo n├úo ├® particular"
- **Solu├º├úo**: Aceitar certificado manualmente no navegador (Avan├ºado ÔåÆ Continuar)

### 8.3 Erro de Compila├º├úo Maven
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\padariaApi
mvn clean install
mvn spring-boot:run "-Dspring.profiles.active=https"
```

### 8.4 Erro de Depend├¬ncias Node.js
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\FrontGoDgital
rm -rf node_modules
npm install
npm run dev:https
```

**Se aparecer erro de TypeScript (moduleResolution):**
```powershell
# Corrigir tsconfig.json automaticamente
(Get-Content tsconfig.json) -replace '"moduleResolution": "bundler"', '"moduleResolution": "node"' | Set-Content tsconfig.json
npm run dev
```

**Alternativas para o Frontend:**
```powershell
# Op├º├úo 1: Script HTTPS configurado
npm run dev:https

# Op├º├úo 2: Definir PORT manualmente
$env:PORT=3443; npm run dev

# Op├º├úo 3: Next.js simples (sem HTTPS)
npm run dev

# Op├º├úo 4: For├ºar porta via vari├ível
$env:NEXT_DEV_PORT=3443; npm run dev
```

### 8.6 Erros de Autentica├º├úo (403 Forbidden)
**Problema:** APIs retornam erro 403 ou dados n├úo carregam
```
Failed to load resource: the server responded with a status of 403 ()
```

**Solu├º├Áes:**
1. **Fazer Login Obrigat├│rio:**
   ```
   Acesse: http://localhost:3000/login
   Email: admin@padaria.com
   Senha: admin123
   ```

2. **Verificar Token no LocalStorage:**
   ```javascript
   // No console do navegador (F12)
   console.log("Token:", localStorage.getItem("accessToken"));
   console.log("User:", localStorage.getItem("user"));
   ```

3. **Limpar Cache e Fazer Login Novamente:**
   ```javascript
   // No console do navegador
   localStorage.clear();
   // Depois acesse /login novamente
   ```

4. **Verificar se Backend est├í Funcionando:**
   ```powershell
   # Testar endpoint de login
   Invoke-WebRequest -Uri "http://localhost:8080/api/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email":"admin@padaria.com","senha":"admin123"}'
   ```
```powershell
cd C:\projects\FIAP\Fase7\Santa-Marcelina\ai_module
pip install --upgrade pip
pip install -r requirements.txt
python ai_service.py
```

## ­ƒôè 9. Monitoramento

### 9.1 Logs dos Servi├ºos
- **AI Service**: Logs no terminal
- **Backend**: Logs no terminal + `padariaApi/logs/`
- **Frontend**: Logs no terminal

### 9.2 Health Checks
```powershell
# Script de monitoramento
while ($true) {
    echo "=== Health Check $(Get-Date) ==="
    curl -k https://localhost:3443 -I
    curl -k https://localhost:5443/health -I
    curl -k https://localhost:8443/actuator/health -I
    Start-Sleep 30
}
```

## ­ƒÄ» 10. Cen├írios de Teste

### 10.1 Teste Completo de Funcionalidade
1. **Iniciar todos os servi├ºos**
2. **Aceitar certificados SSL**
3. **Fazer login no frontend**
4. **Testar funcionalidades principais**
5. **Verificar comunica├º├úo entre servi├ºos**

### 10.2 Teste de Performance
```powershell
# Teste de carga b├ísico (instalar curl se necess├írio)
for ($i=1; $i -le 10; $i++) {
    curl -k https://localhost:8443/api/produtos
    Start-Sleep 1
}
```

## ­ƒÜ¿ 11. Comandos de Emerg├¬ncia

### 11.1 Parar Todos os Servi├ºos
```powershell
# Finalizar processos por porta
$ports = @(3443, 5443, 8443)
foreach ($port in $ports) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($process) {
        Stop-Process -Id $process.OwningProcess -Force
    }
}
```

### 11.2 Reiniciar Ambiente Completo
```powershell
# 1. Parar todos os servi├ºos
# (usar comando acima)

# 2. Limpar cache/builds
cd C:\projects\FIAP\Fase7\Santa-Marcelina\padariaApi
mvn clean

cd C:\projects\FIAP\Fase7\Santa-Marcelina\FrontGoDgital
rm -rf .next

# 3. Reiniciar tudo
.\start_all_services.bat
```

## ­ƒôØ 12. Checklist de Valida├º├úo

- [ ] Java, Node.js, Python instalados
- [ ] Depend├¬ncias instaladas (pip, npm, maven)
- [ ] Certificados SSL presentes
- [ ] AI Service rodando na porta 5443
- [ ] Backend rodando na porta 8443
- [ ] Frontend rodando na porta 3443
- [ ] Certificados aceitos no navegador
- [ ] Login funcionando
- [ ] APIs respondendo
- [ ] Comunica├º├úo entre servi├ºos OK

---

## ­ƒÄë Conclus├úo

Ô£à **SISTEMA HTTPS IMPLEMENTADO COM SUCESSO!**

Seguindo este guia, voc├¬ ter├í todo o sistema funcionando corretamente:

**Configura├º├úo Corporativa (Segura):**
- Ô£à Frontend: HTTP na porta 3000 (sem certificados raiz)
- Ô£à Backend: HTTPS na porta 8443 (aceitar certificado manualmente)
- Ô£à AI Service: HTTPS na porta 5443 (aceitar certificado manualmente)

**Configura├º├úo Pessoal (HTTPS Completo):**
- Ô£à Frontend: HTTPS na porta 3443
- Ô£à Backend: HTTPS na porta 8443
- Ô£à AI Service: HTTPS na porta 5443


**­ƒöæ LOGIN OBRIGAT├ôRIO:**
Para acessar qualquer funcionalidade (Dashboard, Relat├│rios, etc.), voc├¬ DEVE fazer login primeiro:
- ­ƒöù **URL de Login:** http://localhost:3000/login
- ­ƒæñ **Email:** admin@padaria.com  
- ­ƒöÉ **Senha:** admin123


**URLs de Acesso:**
- **Frontend**: http://localhost:3000
- **API**: https://localhost:8443/api
- **AI**: https://localhost:5443/api/ai
