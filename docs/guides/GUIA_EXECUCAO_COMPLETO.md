# 🚀 Guia Completo de Execução - Sistema HTTPS

## 📋 Pré-requisitos

- **Java 17+** instalado
- **Node.js 18+** instalado
- **Python 3.8+** instalado
- **Maven** configurado
- **PowerShell** (Windows)

## 🔧 1. Preparação do Ambiente

### 1.1 Verificar Instalações
```powershell
java -version
node --version
python --version
mvn --version
```

### 1.2 Instalar Dependências Python (AI Module)
```powershell
cd C:\projects\FIAP\Fase6\SRC\ai_module
pip install -r requirements.txt
```

### 1.3 Instalar Dependências Frontend
```powershell
cd C:\projects\FIAP\Fase6\SRC\FrontGoDgital
npm install
```

## 🛡️ 2. Certificados SSL

Os certificados SSL já estão gerados na pasta `ssl_certificates/`:
- `server.crt` - Certificado público
- `server.key` - Chave privada
- `keystore.p12` - Keystore para Spring Boot

## 🚀 3. Inicialização dos Serviços

### 3.1 AI Service (Python Flask) - Porta 5443
```powershell
cd C:\projects\FIAP\Fase6\SRC\ai_module
python ai_service.py
```
**Aguarde** até ver: `Running on https://0.0.0.0:5443`

### 3.2 Backend (Spring Boot) - Porta 8443
**Em um novo terminal PowerShell:**
```powershell
cd C:\projects\FIAP\Fase6\SRC\padariaApi
mvn spring-boot:run "-Dspring.profiles.active=https"
```
**Aguarde** até ver: `Started PadariaApiApplication`

### 3.3 Frontend (React) - Porta 3000
**Em um novo terminal PowerShell:**

⚠️ **Para notebooks corporativos (RECOMENDADO):**
```powershell
cd C:\projects\FIAP\Fase6\SRC\FrontGoDgital
npm start
```
*Inicia a aplicação React completa em HTTP na porta 3000 (sem certificados)*

**Para computadores pessoais (com HTTPS):**
```powershell
cd C:\projects\FIAP\Fase6\SRC\FrontGoDgital
npm run start:https
```
*Inicia a aplicação React em HTTPS na porta 3443 (requer instalação de certificado)*

## 🔍 4. Verificação dos Serviços

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

## 🌐 5. Configuração do Navegador

### 5.1 Aceitar Certificados SSL
1. **Frontend**: Acesse `https://localhost:3443`
   - Clique em "Avançado" 
   - Clique em "Continuar para localhost (não seguro)"

2. **Backend**: Acesse `https://localhost:8443`
   - Clique em "Avançado"
   - Clique em "Continuar para localhost (não seguro)"

3. **AI Service**: Acesse `https://localhost:5443`
   - Clique em "Avançado"
   - Clique em "Continuar para localhost (não seguro)"

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

## ✅ 6. Teste da Aplicação

### 6.1 Teste de Login
**⚠️ IMPORTANTE: FAÇA LOGIN PRIMEIRO!**

1. **Acesse a aplicação React:** `http://localhost:3000`

2. **PRIMEIRO PASSO - LOGIN OBRIGATÓRIO:**
   - 🔗 Clique em "Login" ou acesse diretamente: `http://localhost:3000/login`
   - **Email:** `admin@padaria.com`
   - **Senha:** `admin123`
   - ✅ Clique em "Entrar"
   - 🔄 Você será redirecionado para o dashboard automaticamente

3. **APÓS O LOGIN - Sistema Completo Disponível:**
   - ✅ Dashboard completo com dados reais
   - ✅ Todas as funcionalidades desbloqueadas:
     - 📊 Dashboard & Dashboard Financeiro
     - 🛒 Cadastro de Produtos & Nova Venda
     - 👥 Gerenciamento de Clientes & Usuários
     - 📦 Gestão de Estoque & Categorias
     - 📈 Relatórios & Histórico de Vendas
     - 🤖 Chat IA & Previsão IA
     - ⚙️ Sistema de Backup

4. **⚠️ SEM LOGIN:** 
   - ❌ Você verá erros 403 (Forbidden) nas APIs
   - ❌ Dashboard e relatórios não carregarão dados
   - 🔄 Sistema redirecionará automaticamente para login

3. **APIs Backend (quando iniciadas):**
   - Backend: `https://localhost:8443/api`
   - Swagger: `https://localhost:8443/swagger-ui.html`

### 6.2 Teste de API
```powershell
# Teste básico da API
curl -k -X GET https://localhost:8443/api/produtos

# Teste com autenticação (substitua TOKEN pelo token real)
curl -k -H "Authorization: Bearer TOKEN" https://localhost:8443/api/produtos
```

### 6.3 Teste do AI Service
```powershell
# Teste básico
curl -k -X POST https://localhost:5443/api/ai/chat -H "Content-Type: application/json" -d "{\"message\":\"Olá\"}"
```

## 🛠️ 7. Scripts de Inicialização Automática

### 7.1 Script para Todos os Serviços
```powershell
# Criar arquivo: start_all_services.bat
@echo off
echo Iniciando todos os serviços HTTPS...

start "AI Service" cmd /k "cd /d C:\projects\FIAP\Fase6\SRC\ai_module && python ai_service.py"
timeout /t 5 /nobreak > nul

start "Backend" cmd /k "cd /d C:\projects\FIAP\Fase6\SRC\padariaApi && mvn spring-boot:run \"-Dspring.profiles.active=https\""
timeout /t 10 /nobreak > nul

start "Frontend" cmd /k "cd /d C:\projects\FIAP\Fase6\SRC\FrontGoDgital && npm start"

echo Todos os serviços foram iniciados!
echo Frontend: https://localhost:3443
echo Backend: https://localhost:8443
echo AI Service: https://localhost:5443
pause
```

### 7.2 Executar Script
```powershell
cd C:\projects\FIAP\Fase6\SRC
.\start_all_services.bat
```

## 🔧 8. Solução de Problemas

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
- **Erro**: "Sua conexão não é particular"
- **Solução**: Aceitar certificado manualmente no navegador (Avançado → Continuar)

### 8.3 Erro de Compilação Maven
```powershell
cd C:\projects\FIAP\Fase6\SRC\padariaApi
mvn clean install
mvn spring-boot:run "-Dspring.profiles.active=https"
```

### 8.4 Erro de Dependências Node.js
```powershell
cd C:\projects\FIAP\Fase6\SRC\FrontGoDgital
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
# Opção 1: Script HTTPS configurado
npm run dev:https

# Opção 2: Definir PORT manualmente
$env:PORT=3443; npm run dev

# Opção 3: Next.js simples (sem HTTPS)
npm run dev

# Opção 4: Forçar porta via variável
$env:NEXT_DEV_PORT=3443; npm run dev
```

### 8.6 Erros de Autenticação (403 Forbidden)
**Problema:** APIs retornam erro 403 ou dados não carregam
```
Failed to load resource: the server responded with a status of 403 ()
```

**Soluções:**
1. **Fazer Login Obrigatório:**
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

4. **Verificar se Backend está Funcionando:**
   ```powershell
   # Testar endpoint de login
   Invoke-WebRequest -Uri "http://localhost:8080/api/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email":"admin@padaria.com","senha":"admin123"}'
   ```
```powershell
cd C:\projects\FIAP\Fase6\SRC\ai_module
pip install --upgrade pip
pip install -r requirements.txt
python ai_service.py
```

## 📊 9. Monitoramento

### 9.1 Logs dos Serviços
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

## 🎯 10. Cenários de Teste

### 10.1 Teste Completo de Funcionalidade
1. **Iniciar todos os serviços**
2. **Aceitar certificados SSL**
3. **Fazer login no frontend**
4. **Testar funcionalidades principais**
5. **Verificar comunicação entre serviços**

### 10.2 Teste de Performance
```powershell
# Teste de carga básico (instalar curl se necessário)
for ($i=1; $i -le 10; $i++) {
    curl -k https://localhost:8443/api/produtos
    Start-Sleep 1
}
```

## 🚨 11. Comandos de Emergência

### 11.1 Parar Todos os Serviços
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
# 1. Parar todos os serviços
# (usar comando acima)

# 2. Limpar cache/builds
cd C:\projects\FIAP\Fase6\SRC\padariaApi
mvn clean

cd C:\projects\FIAP\Fase6\SRC\FrontGoDgital
rm -rf .next

# 3. Reiniciar tudo
.\start_all_services.bat
```

## 📝 12. Checklist de Validação

- [ ] Java, Node.js, Python instalados
- [ ] Dependências instaladas (pip, npm, maven)
- [ ] Certificados SSL presentes
- [ ] AI Service rodando na porta 5443
- [ ] Backend rodando na porta 8443
- [ ] Frontend rodando na porta 3443
- [ ] Certificados aceitos no navegador
- [ ] Login funcionando
- [ ] APIs respondendo
- [ ] Comunicação entre serviços OK

---

## 🎉 Conclusão

✅ **SISTEMA HTTPS IMPLEMENTADO COM SUCESSO!**

Seguindo este guia, você terá todo o sistema funcionando corretamente:

**Configuração Corporativa (Segura):**
- ✅ Frontend: HTTP na porta 3000 (sem certificados raiz)
- ✅ Backend: HTTPS na porta 8443 (aceitar certificado manualmente)
- ✅ AI Service: HTTPS na porta 5443 (aceitar certificado manualmente)

**Configuração Pessoal (HTTPS Completo):**
- ✅ Frontend: HTTPS na porta 3443
- ✅ Backend: HTTPS na porta 8443
- ✅ AI Service: HTTPS na porta 5443


**🔑 LOGIN OBRIGATÓRIO:**
Para acessar qualquer funcionalidade (Dashboard, Relatórios, etc.), você DEVE fazer login primeiro:
- 🔗 **URL de Login:** http://localhost:3000/login
- 👤 **Email:** admin@padaria.com  
- 🔐 **Senha:** admin123


**URLs de Acesso:**
- **Frontend**: http://localhost:3000
- **API**: https://localhost:8443/api
- **AI**: https://localhost:5443/api/ai