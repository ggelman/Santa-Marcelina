# 🛠️ DOCUMENTAÇÃO TÉCNICA CONSOLIDADA
> **Sistema Padaria Santa Marcelina** | Setup e Configuração Completa

---

## 🎯 **EXECUÇÃO RÁPIDA** (Uso Imediato)

```batch
# MÉTODO 1: Automático (Recomendado)
cd C:\projects\FIAP\Fase6\SRC
.\start_all_services_correto.bat

# MÉTODO 2: Manual (Emergência)
# Terminal 1: cd ai_module && python ai_service.py
# Terminal 2: cd padariaApi && mvn spring-boot:run "-Dspring.profiles.active=https"
# Terminal 3: cd FrontGoDgital && npm start
```

**🔐 Acesso:** http://localhost:3000 | `admin@padaria.com` / `admin123`

---

## 🏗️ **ARQUITETURA TÉCNICA**

### 📊 **Stack Tecnológico**
```
🌐 Frontend          ⚙️ Backend           🤖 AI Service
React 18 + Next.js   Spring Boot 3.x     Python 3.8+ Flask
Port: 3000           Port: 8443          Port: 5443
Styled Components    MySQL + H2          Gemini AI + Redis
Context API          JWT + Security       Cache + ML Models
```

### 🔗 **Comunicação entre Serviços**
```
Frontend ←→ Backend (HTTPS/8443) ←→ AI Service (HTTPS/5443)
    ↓
MySQL Database (3306)
Redis Cache (6379) [Opcional]
```

### 📁 **Estrutura de Pastas**
```
📦 SRC/
├── 🌐 FrontGoDgital/           # React + Next.js
│   ├── src/components/         # Componentes React
│   ├── src/pages/             # Páginas da aplicação
│   ├── src/contexts/          # Context API
│   ├── public/                # Assets estáticos
│   └── package.json           # Dependências Node
├── ⚙️ padariaApi/              # Spring Boot
│   ├── src/main/java/         # Código Java
│   ├── src/main/resources/    # Configurações
│   └── pom.xml               # Dependências Maven
├── 🤖 ai_module/               # Python Flask
│   ├── ai_service.py          # Serviço principal
│   ├── requirements.txt       # Dependências Python
│   ├── trained_models/        # Modelos ML treinados
│   └── fallback_data/         # Dados de backup
├── 🔒 ssl_certificates/        # Certificados HTTPS
├── 📂 fallback_data/           # Dados demo sistema
└── 📚 docs/                    # Documentação técnica
```

---

## ⚙️ **CONFIGURAÇÃO DETALHADA**

### 🐍 **AI Service (Python)**

**Dependências Principais:**
```python
flask==2.3.2
flask-cors==4.0.0
flask-limiter==3.4.0
google-generativeai==0.7.2
pandas==2.0.3
numpy==1.24.3
redis==4.6.0
prophet==1.1.4
```

**Configuração:**
```python
# ai_service.py (Principais configurações)
app.config['LIMITER_STORAGE_URL'] = 'memory://'
CORS(app, origins=['http://localhost:3000'])
ssl_context = ('server.crt', 'server.key')
app.run(host='0.0.0.0', port=5443, ssl_context=ssl_context)
```

### ☕ **Backend (Spring Boot)**

**Configuração HTTPS (application-https.yml):**
```yaml
server:
  port: 8443
  ssl:
    key-store: classpath:keystore.p12
    key-store-password: padaria123
    key-store-type: PKCS12
    key-alias: padaria

spring:
  profiles:
    active: https
  datasource:
    url: jdbc:mysql://localhost:3306/padaria_db
    username: root
    password: root
```

**Principais Dependências (pom.xml):**
```xml
<spring-boot.version>3.1.0</spring-boot.version>
spring-boot-starter-web
spring-boot-starter-security
spring-boot-starter-data-jpa
mysql-connector-java
```

### ⚛️ **Frontend (React)**

**Dependências Principais (package.json):**
```json
{
  "next": "14.2.15",
  "react": "18.3.1",
  "styled-components": "6.1.13",
  "axios": "1.7.7",
  "react-router-dom": "6.26.2"
}
```

**Configuração API (contexts/AuthContext.js):**
```javascript
const API_BASE_URL = 'https://localhost:8443/api'
const AI_API_BASE_URL = 'https://localhost:5443/api'
```

---

## 🔒 **CONFIGURAÇÃO HTTPS/SSL**

### 🛡️ **Certificados SSL**

**Estrutura de Certificados:**
```
ssl_certificates/
├── server.crt          # Certificado público (AI Service)
├── server.key          # Chave privada (AI Service)  
├── keystore.p12        # Keystore Java (Backend)
└── certificados.md     # Documentação dos certificados
```

**Gerar Novos Certificados:**
```powershell
# Windows
.\generate_ssl_certs.ps1

# Linux/Mac  
./generate_ssl_certs.sh
```

### 🔧 **Perfis de Execução**

| Perfil | Porta | Certificado | Uso |
|--------|-------|-------------|-----|
| `development` | 8080 | Sem SSL | Desenvolvimento local |
| `https` | 8443 | keystore.p12 | Produção/HTTPS |
| `test` | Random | H2 Memory | Testes automatizados |

---

## 🗄️ **CONFIGURAÇÃO BANCO DE DADOS**

### 🐬 **MySQL (Produção)**
```sql
-- Criar banco
CREATE DATABASE padaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usuário específico  
CREATE USER 'padaria_user'@'localhost' IDENTIFIED BY 'padaria_pass';
GRANT ALL PRIVILEGES ON padaria_db.* TO 'padaria_user'@'localhost';
FLUSH PRIVILEGES;
```

### 🗃️ **H2 Database (Desenvolvimento)**
```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
  h2:
    console:
      enabled: true
      path: /h2-console
```

---

## 🚀 **DEPLOY E PRODUÇÃO**

### 📦 **Build para Produção**

**Frontend:**
```bash
cd FrontGoDgital
npm run build
npm run export  # Para deploy estático
```

**Backend:**
```bash  
cd padariaApi
mvn clean package -Dspring.profiles.active=prod
java -jar target/padaria-api-1.0.jar
```

**AI Service:**
```bash
cd ai_module
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5443 --certfile=server.crt --keyfile=server.key ai_service:app
```

### 🌐 **Variáveis de Ambiente (Produção)**
```bash
# Backend
export SPRING_PROFILES_ACTIVE=prod
export DB_HOST=your-mysql-host
export DB_USER=your-db-user  
export DB_PASS=your-db-pass
export JWT_SECRET=your-jwt-secret

# AI Service
export GEMINI_API_KEY=your-gemini-key
export REDIS_URL=your-redis-url
export FLASK_ENV=production
```

---

## 🧪 **TESTES**

### ✅ **Executar Testes**
```bash
# Backend (JUnit)
cd padariaApi  
mvn test

# Frontend (Jest)
cd FrontGoDgital
npm test

# AI Service (pytest)
cd ai_module
python -m pytest tests/
```

### 🔍 **Verificação de Saúde**
```bash
# Health checks
curl -k https://localhost:8443/actuator/health
curl -k https://localhost:5443/health
curl http://localhost:3000
```

---

## 🐛 **DEBUGGING**

### 📊 **Logs do Sistema**
```bash
# Backend logs
tail -f padariaApi/logs/application.log

# AI Service logs  
tail -f ai_module/ai_service.log

# Frontend logs (console do navegador)
F12 → Console
```

### 🔧 **Problemas Comuns**

| Erro | Causa | Solução |
|------|-------|---------|
| `Port already in use` | Porta ocupada | `stop_all_services.bat` |
| `SSL handshake failed` | Certificado não aceito | Aceitar no navegador |
| `Connection refused` | Serviço não iniciado | Verificar startup logs |
| `404 Not Found` | Endpoint inexistente | Verificar mapeamento |
| `401 Unauthorized` | Token inválido | Refazer login |

---

## 📈 **MONITORAMENTO**

### 📊 **Métricas Disponíveis**
- **Backend:** Actuator endpoints (`/actuator/metrics`)
- **AI Service:** Logs estruturados + Redis metrics  
- **Frontend:** Performance API + Error tracking

### 🚨 **Alertas de Sistema**
- Rate limiting excedido
- SSL certificate expirando
- Disk space baixo
- Falhas de conectividade

---

## 🔄 **MANUTENÇÃO**

### 🧹 **Limpeza Periódica**
```bash
# Limpar logs antigos (> 30 dias)
find . -name "*.log" -mtime +30 -delete

# Limpar cache do Redis
redis-cli FLUSHALL

# Limpar build artifacts
mvn clean (Backend)
npm run clean (Frontend)
```

### 📅 **Tarefas de Manutenção**
- **Diário:** Verificar logs de erro
- **Semanal:** Backup do banco de dados  
- **Mensal:** Atualizar certificados SSL
- **Trimestral:** Atualizar dependências

---

## 📞 **SUPORTE TÉCNICO**

### 🆘 **Contatos de Emergência**
- **Sistema crítico:** Restart automático via `start_all_services_correto.bat`
- **Problemas SSL:** Regenerar certificados
- **Falha de BD:** Backup automático + restore

### 📋 **Informações para Suporte**
```bash
# Coleta de informações do sistema
java -version > system_info.txt
node --version >> system_info.txt  
python --version >> system_info.txt
netstat -an | findstr ":3000\|:8443\|:5443" >> system_info.txt
```

---

*📅 Última atualização: Outubro 2025 | 🔧 Configuração consolidada e otimizada*