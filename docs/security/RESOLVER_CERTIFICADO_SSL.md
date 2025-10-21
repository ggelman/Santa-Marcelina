# 🔧 Guia de Resolução: "Your connection isn't private"

## 🎯 **Solução Rápida para o Erro de Certificado**

### **1. Aceitar Certificado no Chrome/Edge:**
Quando ver a tela "Your connection isn't private":

1. **Clique em "Advanced" (Avançado)**
2. **Clique em "Proceed to localhost (unsafe)"**
3. **Repita para cada URL HTTPS**

### **2. URLs para Aceitar Certificados:**
Visite cada uma e aceite o certificado:

- ✅ **Frontend**: https://localhost:3443
- ✅ **AI Service**: https://localhost:5443/api/health  
- ⚠️ **Backend**: https://localhost:8443/api (quando estiver rodando)

## 🚀 **Verificação dos Serviços**

### **Serviços Atualmente Rodando:**
- ✅ **AI Service**: porta 5443 (Python/Flask)
- ✅ **Frontend**: porta 3443 (React/Next.js)
- ❌ **Backend**: porta 8443 (Spring Boot) - Precisa iniciar

### **Comandos para Verificar Status:**
```powershell
# Verificar portas ativas
Get-NetTCPConnection | Where-Object {$_.LocalPort -in @(3443, 5443, 8443) -and $_.State -eq "Listen"}

# Testar serviços
curl -k https://localhost:5443/api/health  # AI Service
curl -k https://localhost:3443            # Frontend
curl -k https://localhost:8443/api        # Backend
```

## 🔄 **Como Iniciar os Serviços Individualmente**

### **1. AI Service (já rodando ✅)**
```batch
cd ai_module
set USE_HTTPS=true
set AI_SERVICE_PORT=5443
python ai_service.py
```

### **2. Frontend (já rodando ✅)**
```batch
cd FrontGoDgital
npm run start:https
```

### **3. Backend (precisa iniciar ❌)**
```batch
cd padariaApi
mvn spring-boot:run -Dspring.profiles.active=https
```

## 🔒 **Por que isso acontece?**

### **Certificados Self-Signed:**
- São certificados criados localmente
- Não são assinados por uma Autoridade Certificadora (CA)
- **Seguros para desenvolvimento**, mas browsers alertam
- **Normal** em ambiente de desenvolvimento

### **O que o browser está fazendo:**
- ✅ **Protegendo você** de certificados não verificados
- ⚠️ **Avisando** que é um certificado self-signed
- 🔒 **Ainda criptografa** a comunicação após aceitar

## 🛠️ **Resolução Alternativa: Adicionar Certificado ao Sistema**

### **Para Windows (Opcional):**
```powershell
# Abrir Gerenciador de Certificados
certlm.msc

# Importar ssl_certificates/server.crt em:
# Certificados > Autoridades de Certificação Raiz Confiáveis
```

### **Para Chrome (Opcional):**
1. Configurações → Privacidade e segurança → Segurança
2. Gerenciar certificados → Autoridades certificadoras raiz confiáveis
3. Importar → Selecionar `ssl_certificates/server.crt`

## ✅ **Verificação Final**

### **Depois de aceitar os certificados, você deve ver:**
- 🌐 **Frontend**: Interface da aplicação em https://localhost:3443
- 🔧 **AI Service**: Health check em https://localhost:5443/api/health
- 📊 **Backend**: API endpoints em https://localhost:8443/api

### **Status esperado no browser:**
- 🔒 **Ícone de cadeado** (pode ter aviso amarelo para self-signed)
- ✅ **Conexão HTTPS funcionando**
- 🛡️ **Dados criptografados**

## 🎉 **Conclusão**

**Este erro é NORMAL e ESPERADO com certificados self-signed!**

1. ✅ **Aceite o certificado** clicando "Advanced" → "Proceed"
2. ✅ **Repita para cada serviço** (3443, 5443, 8443)
3. ✅ **Aplicação funcionará normalmente** após aceitar

**🔐 A comunicação estará totalmente criptografada e segura!**