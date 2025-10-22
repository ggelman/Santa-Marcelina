# ­ƒøá´©Å DOCUMENTA├ç├âO T├ëCNICA CONSOLIDADA
> **Sistema Padaria Santa Marcelina** | Setup e Configura├º├úo Completa

---

## ­ƒÄ» **EXECU├ç├âO R├üPIDA** (Uso Imediato)

```batch
# M├ëTODO 1: Autom├ítico (Recomendado)
cd C:\projects\FIAP\Fase7\Santa-Marcelina
.\start_all_services_correto.bat

# M├ëTODO 2: Manual (Emerg├¬ncia)
# Terminal 1: cd ai_module && python ai_service.py
# Terminal 2: cd padariaApi && mvn spring-boot:run "-Dspring.profiles.active=https"
# Terminal 3: cd FrontGoDgital && npm start
```

**­ƒöÉ Acesso:** http://localhost:3000 | `admin@padaria.com` / `admin123`

---

## ­ƒÅù´©Å **ARQUITETURA T├ëCNICA**

### ­ƒôè **Stack Tecnol├│gico**
```
­ƒîÉ Frontend          ÔÜÖ´©Å Backend           ­ƒñû AI Service
React 18 + Next.js   Spring Boot 3.x     Python 3.8+ Flask
Port: 3000           Port: 8443          Port: 5443
Styled Components    MySQL + H2          Gemini AI + Redis
Context API          JWT + Security       Cache + ML Models
```

### ­ƒöù **Comunica├º├úo entre Servi├ºos**
```
Frontend ÔåÉÔåÆ Backend (HTTPS/8443) ÔåÉÔåÆ AI Service (HTTPS/5443)
    Ôåô
MySQL Database (3306)
Redis Cache (6379) [Opcional]
```

### ­ƒôü **Estrutura de Pastas**
```
­ƒôª SRC/
Ôö£ÔöÇÔöÇ ­ƒîÉ FrontGoDgital/           # React + Next.js
Ôöé   Ôö£ÔöÇÔöÇ src/components/         # Componentes React
Ôöé   Ôö£ÔöÇÔöÇ src/pages/             # P├íginas da aplica├º├úo
Ôöé   Ôö£ÔöÇÔöÇ src/contexts/          # Context API
Ôöé   Ôö£ÔöÇÔöÇ public/                # Assets est├íticos
Ôöé   ÔööÔöÇÔöÇ package.json           # Depend├¬ncias Node
Ôö£ÔöÇÔöÇ ÔÜÖ´©Å padariaApi/              # Spring Boot
Ôöé   Ôö£ÔöÇÔöÇ src/main/java/         # C├│digo Java
Ôöé   Ôö£ÔöÇÔöÇ src/main/resources/    # Configura├º├Áes
Ôöé   ÔööÔöÇÔöÇ pom.xml               # Depend├¬ncias Maven
Ôö£ÔöÇÔöÇ ­ƒñû ai_module/               # Python Flask
Ôöé   Ôö£ÔöÇÔöÇ ai_service.py          # Servi├ºo principal
Ôöé   Ôö£ÔöÇÔöÇ requirements.txt       # Depend├¬ncias Python
Ôöé   Ôö£ÔöÇÔöÇ trained_models/        # Modelos ML treinados
Ôöé   ÔööÔöÇÔöÇ fallback_data/         # Dados de backup
Ôö£ÔöÇÔöÇ ­ƒöÆ ssl_certificates/        # Certificados HTTPS
Ôö£ÔöÇÔöÇ ­ƒôé fallback_data/           # Dados demo sistema
ÔööÔöÇÔöÇ ­ƒôÜ docs/                    # Documenta├º├úo t├®cnica
```

---

## ÔÜÖ´©Å **CONFIGURA├ç├âO DETALHADA**

### ­ƒÉì **AI Service (Python)**

**Depend├¬ncias Principais:**
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

**Configura├º├úo:**
```python
# ai_service.py (Principais configura├º├Áes)
app.config['LIMITER_STORAGE_URL'] = 'memory://'
CORS(app, origins=['http://localhost:3000'])
ssl_context = ('server.crt', 'server.key')
app.run(host='0.0.0.0', port=5443, ssl_context=ssl_context)
```

### Ôÿò **Backend (Spring Boot)**

**Configura├º├úo HTTPS (application-https.yml):**
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

**Principais Depend├¬ncias (pom.xml):**
```xml
<spring-boot.version>3.1.0</spring-boot.version>
spring-boot-starter-web
spring-boot-starter-security
spring-boot-starter-data-jpa
mysql-connector-java
```

### ÔÜø´©Å **Frontend (React)**

**Depend├¬ncias Principais (package.json):**
```json
{
  "next": "14.2.15",
  "react": "18.3.1",
  "styled-components": "6.1.13",
  "axios": "1.7.7",
  "react-router-dom": "6.26.2"
}
```

**Configura├º├úo API (contexts/AuthContext.js):**
```javascript
const API_BASE_URL = 'https://localhost:8443/api'
const AI_API_BASE_URL = 'https://localhost:5443/api'
```

---

## ­ƒöÆ **CONFIGURA├ç├âO HTTPS/SSL**

### ­ƒøí´©Å **Certificados SSL**

**Estrutura de Certificados:**
```
ssl_certificates/
Ôö£ÔöÇÔöÇ server.crt          # Certificado p├║blico (AI Service)
Ôö£ÔöÇÔöÇ server.key          # Chave privada (AI Service)  
Ôö£ÔöÇÔöÇ keystore.p12        # Keystore Java (Backend)
ÔööÔöÇÔöÇ certificados.md     # Documenta├º├úo dos certificados
```

**Gerar Novos Certificados:**
```powershell
# Windows
.\generate_ssl_certs.ps1

# Linux/Mac  
./generate_ssl_certs.sh
```

### ­ƒöº **Perfis de Execu├º├úo**

| Perfil | Porta | Certificado | Uso |
|--------|-------|-------------|-----|
| `development` | 8080 | Sem SSL | Desenvolvimento local |
| `https` | 8443 | keystore.p12 | Produ├º├úo/HTTPS |
| `test` | Random | H2 Memory | Testes automatizados |

---

## ­ƒùä´©Å **CONFIGURA├ç├âO BANCO DE DADOS**

### ­ƒÉ¼ **MySQL (Produ├º├úo)**
```sql
-- Criar banco
CREATE DATABASE padaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usu├írio espec├¡fico  
CREATE USER 'padaria_user'@'localhost' IDENTIFIED BY 'padaria_pass';
GRANT ALL PRIVILEGES ON padaria_db.* TO 'padaria_user'@'localhost';
FLUSH PRIVILEGES;
```

### ­ƒùâ´©Å **H2 Database (Desenvolvimento)**
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

## ­ƒÜÇ **DEPLOY E PRODU├ç├âO**

### ­ƒôª **Build para Produ├º├úo**

**Frontend:**
```bash
cd FrontGoDgital
npm run build
npm run export  # Para deploy est├ítico
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

### ­ƒîÉ **Vari├íveis de Ambiente (Produ├º├úo)**
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

## ­ƒº¬ **TESTES**

### Ô£à **Executar Testes**
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

### ­ƒöì **Verifica├º├úo de Sa├║de**
```bash
# Health checks
curl -k https://localhost:8443/actuator/health
curl -k https://localhost:5443/health
curl http://localhost:3000
```

---

## ­ƒÉø **DEBUGGING**

### ­ƒôè **Logs do Sistema**
```bash
# Backend logs
tail -f padariaApi/logs/application.log

# AI Service logs  
tail -f ai_module/ai_service.log

# Frontend logs (console do navegador)
F12 ÔåÆ Console
```

### ­ƒöº **Problemas Comuns**

| Erro | Causa | Solu├º├úo |
|------|-------|---------|
| `Port already in use` | Porta ocupada | `stop_all_services.bat` |
| `SSL handshake failed` | Certificado n├úo aceito | Aceitar no navegador |
| `Connection refused` | Servi├ºo n├úo iniciado | Verificar startup logs |
| `404 Not Found` | Endpoint inexistente | Verificar mapeamento |
| `401 Unauthorized` | Token inv├ílido | Refazer login |

---

## ­ƒôê **MONITORAMENTO**

### ­ƒôè **M├®tricas Dispon├¡veis**
- **Backend:** Actuator endpoints (`/actuator/metrics`)
- **AI Service:** Logs estruturados + Redis metrics  
- **Frontend:** Performance API + Error tracking

### ­ƒÜ¿ **Alertas de Sistema**
- Rate limiting excedido
- SSL certificate expirando
- Disk space baixo
- Falhas de conectividade

---

## ­ƒöä **MANUTEN├ç├âO**

### ­ƒº╣ **Limpeza Peri├│dica**
```bash
# Limpar logs antigos (> 30 dias)
find . -name "*.log" -mtime +30 -delete

# Limpar cache do Redis
redis-cli FLUSHALL

# Limpar build artifacts
mvn clean (Backend)
npm run clean (Frontend)
```

### ­ƒôà **Tarefas de Manuten├º├úo**
- **Di├írio:** Verificar logs de erro
- **Semanal:** Backup do banco de dados  
- **Mensal:** Atualizar certificados SSL
- **Trimestral:** Atualizar depend├¬ncias

---

## ­ƒô× **SUPORTE T├ëCNICO**

### ­ƒåÿ **Contatos de Emerg├¬ncia**
- **Sistema cr├¡tico:** Restart autom├ítico via `start_all_services_correto.bat`
- **Problemas SSL:** Regenerar certificados
- **Falha de BD:** Backup autom├ítico + restore

### ­ƒôï **Informa├º├Áes para Suporte**
```bash
# Coleta de informa├º├Áes do sistema
java -version > system_info.txt
node --version >> system_info.txt  
python --version >> system_info.txt
netstat -an | findstr ":3000\|:8443\|:5443" >> system_info.txt
```

---

*­ƒôà ├Ültima atualiza├º├úo: Outubro 2025 | ­ƒöº Configura├º├úo consolidada e otimizada*
