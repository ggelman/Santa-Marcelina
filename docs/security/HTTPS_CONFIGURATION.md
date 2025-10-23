# 🔒 Configuração HTTPS - Documentação Completa

## Visão Geral
Esta documentação detalha a implementação de HTTPS em todos os componentes do sistema GoDigital Bakery, garantindo comunicação segura entre Frontend, Backend e AI Module.

## 📋 Resumo da Implementação

### ✅ Certificados SSL Gerados
- **Localização**: `ssl_certificates/`
- **Arquivos**:
  - `server.key` - Chave privada (2048 bits)
  - `server.crt` - Certificado público (válido por 365 dias)
  - `server.pem` - Formato PEM para Python/Flask
  - `keystore.p12` - Keystore para Java/Spring Boot
- **Senha do Keystore**: `padaria123`
- **Válido para**: localhost

### 🔗 Portas HTTPS Configuradas
| Componente | Porta HTTP | Porta HTTPS | Status |
|------------|------------|-------------|---------|
| Frontend (React/Next.js) | 3000 | **3443** | ✅ Funcionando |
| Backend (Spring Boot) | 8080 | **8443** | ✅ Configurado |
| AI Module (Python/Flask) | 5001 | **5443** | ✅ Funcionando |

## 🛠️ Configurações por Componente

### 1. AI Module (Python/Flask)

#### Arquivo: `ai_service.py`
```python
def get_ssl_context():
    """Configura o contexto SSL para HTTPS."""
    import ssl
    import os
    
    # Caminhos dos certificados SSL
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_dir = os.path.join(base_dir, 'ssl_certificates')
    cert_file = os.path.join(cert_dir, 'server.crt')
    key_file = os.path.join(cert_dir, 'server.key')
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    return context

if __name__ == '__main__':
    use_https = os.getenv('USE_HTTPS', 'true').lower() == 'true'
    port = int(os.getenv('AI_SERVICE_PORT', '5443' if use_https else '5001'))
    
    if use_https:
        ssl_context = get_ssl_context()
        app.run(host='0.0.0.0', port=port, debug=True, ssl_context=ssl_context)
```

#### Script de Inicialização: `start_ai_https.bat`
```batch
set USE_HTTPS=true
set AI_SERVICE_PORT=5443
python ai_service.py
```

### 2. Backend (Spring Boot)

#### Arquivo: `application-https.properties`
```properties
server.port=8443
server.ssl.enabled=true
server.ssl.key-store=C:/projects/FIAP/Fase6/SRC/ssl_certificates/keystore.p12
server.ssl.key-store-password=padaria123
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=localhost
server.ssl.protocol=TLS
server.ssl.enabled-protocols=TLSv1.2,TLSv1.3

ai.service.url=https://localhost:5443/api/ai
```

#### Configuração SSL no Controller: `IAController.java`
```java
@CrossOrigin(origins = {"http://localhost:3000", "https://localhost:3443"})
@Value("${ai.service.url}")
private String aiServiceUrl;
```

#### Script de Inicialização: `start_backend_https.bat`
```batch
mvn spring-boot:run -Dspring.profiles.active=https
```

### 3. Frontend (React/Next.js)

#### Arquivo: `package.json`
```json
{
  "scripts": {
    "dev:https": "next dev --port 3443 --experimental-https",
    "start:https": "set HTTPS=true&&set SSL_CRT_FILE=../ssl_certificates/server.crt&&set SSL_KEY_FILE=../ssl_certificates/server.key&&set PORT=3443&&react-scripts start"
  }
}
```

#### Configuração da API: `src/services/api.js`
```javascript
const api = axios.create({
  baseURL: "https://localhost:8443/api",
  timeout: 30000,
  httpsAgent: process.env.NODE_ENV === 'development' ? 
    new (require('https').Agent)({ rejectUnauthorized: false }) : undefined
})
```

#### Script de Inicialização: `start_frontend_https.bat`
```batch
set HTTPS=true
set SSL_CRT_FILE=..\ssl_certificates\server.crt
set SSL_KEY_FILE=..\ssl_certificates\server.key
set PORT=3443
npm run start:https
```

## 🚀 Como Iniciar os Serviços com HTTPS

### 1. Gerar Certificados (Uma vez)
```powershell
# Execute no diretório raiz
PowerShell -ExecutionPolicy Bypass -File "generate_certs.ps1"
```

### 2. Iniciar AI Service com HTTPS
```batch
# Opção 1: Script automático
start_ai_https.bat

# Opção 2: Manual
cd ai_module
set USE_HTTPS=true
set AI_SERVICE_PORT=5443
python ai_service.py
```

### 3. Iniciar Backend com HTTPS
```batch
# Opção 1: Script automático
start_backend_https.bat

# Opção 2: Manual
cd synvia-core
mvn spring-boot:run -Dspring.profiles.active=https
```

### 4. Iniciar Frontend com HTTPS
```batch
# Opção 1: Script automático
start_frontend_https.bat

# Opção 2: Manual
cd FrontGoDgital
npm run start:https
```

## 🔗 URLs de Acesso HTTPS

### Aplicação Principal
- **Frontend**: https://localhost:3443
- **Backend API**: https://localhost:8443/api
- **AI Service**: https://localhost:5443/api

### Endpoints de Documentação
- **API Documentation**: https://localhost:5443/docs (AI Service)
- **Health Check**: https://localhost:5443/api/health

## 🛡️ Configurações de Segurança

### Certificados Self-Signed
- **Uso**: Desenvolvimento local apenas
- **Validade**: 365 dias
- **Algoritmo**: RSA 2048 bits
- **Subject**: `/C=BR/ST=SP/L=Sao Paulo/O=GoDigital/OU=Development/CN=localhost`

### Configurações SSL/TLS
- **Protocolos suportados**: TLSv1.2, TLSv1.3
- **Formato de certificados**: 
  - PEM para Python/Flask
  - PKCS12 para Java/Spring Boot
  - CRT/KEY para React

### Tratamento de Certificados Self-Signed
- **Browser**: Aceitar exceção de segurança manualmente
- **RestTemplate (Java)**: Configurado para aceitar certificados não verificados
- **Axios (JavaScript)**: Configurado `rejectUnauthorized: false` em desenvolvimento

## 📝 Configurações Específicas

### Variáveis de Ambiente
```bash
# AI Service
USE_HTTPS=true
AI_SERVICE_PORT=5443

# Frontend
HTTPS=true
SSL_CRT_FILE=../ssl_certificates/server.crt
SSL_KEY_FILE=../ssl_certificates/server.key
PORT=3443

# Backend (via profiles)
spring.profiles.active=https
```

### CORS - Cross-Origin Resource Sharing
```java
// Backend permite ambos HTTP e HTTPS do frontend
@CrossOrigin(origins = {"http://localhost:3000", "https://localhost:3443"})
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. "Certificado não encontrado"
```bash
# Verificar se os certificados existem
ls ssl_certificates/
# Deve listar: server.crt, server.key, server.pem, keystore.p12
```

#### 2. "Conexão SSL falhou"
- Verificar se os caminhos dos certificados estão corretos
- Confirmar que a senha do keystore está correta (`padaria123`)
- Validar se as portas HTTPS não estão em uso

#### 3. "CORS error"
- Verificar se o backend permite origem HTTPS
- Confirmar configuração `@CrossOrigin` nos controllers

#### 4. "Certificate not trusted"
- No browser: Clicar "Advanced" → "Proceed to localhost (unsafe)"
- É normal com certificados self-signed

## 🔄 Migração de HTTP para HTTPS

### URLs Atualizadas
```javascript
// ANTES (HTTP)
http://localhost:3000  → https://localhost:3443  (Frontend)
http://localhost:8080  → https://localhost:8443  (Backend)
http://localhost:5001  → https://localhost:5443  (AI Service)

// DEPOIS (HTTPS)
Frontend → Backend: https://localhost:8443/api
Backend → AI Service: https://localhost:5443/api/ai
```

## 📈 Próximos Passos (Produção)

### Para ambiente de produção, considere:

1. **Certificados válidos** (Let's Encrypt, CA comercial)
2. **Reverse proxy** (Nginx, Apache)
3. **Load balancer** com terminação SSL
4. **Secrets management** para senhas
5. **Monitoramento SSL** (expiração de certificados)

## ✅ Status da Implementação

- [x] Certificados SSL gerados
- [x] AI Module configurado com HTTPS
- [x] Backend configurado com HTTPS  
- [x] Frontend configurado com HTTPS
- [x] URLs atualizadas entre serviços
- [x] Scripts de inicialização criados
- [x] Documentação completa

---

**🔒 Implementação HTTPS concluída com sucesso!**

*Todos os componentes do sistema GoDigital Bakery agora suportam comunicação segura via HTTPS.*
