﻿# ðŸš€ Guia Completo de ExecuÃ§Ã£o

Procedimento detalhado para preparar e executar todos os mÃ³dulos do goDigital Code com HTTPS opcional e validaÃ§Ãµes pÃ³s-start.

---

## 1. PrÃ©-requisitos

| Componente | VersÃ£o recomendada | VerificaÃ§Ã£o |
| --- | --- | --- |
| Java | 17 ou superior | `java -version` |
| Maven | 3.8 ou superior | `mvn -version` |
| Node.js | 18 LTS | `node --version` |
| npm | 8 ou superior | `npm --version` |
| Python | 3.10 ou superior | `python --version` |

> Dica: em Windows, instale o [WSL](https://learn.microsoft.com/windows/wsl/install) para uma experiÃªncia mais prÃ³xima ao ambiente de produÃ§Ã£o.

---

## 2. PreparaÃ§Ã£o do ambiente

### 2.1 DependÃªncias do mÃ³dulo de IA
```bash
cd ai_module
python -m venv .venv  # opcional
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```
- Copie `ai_module/.env.example` para `ai_module/.env` e ajuste credenciais/APIs quando necessÃ¡rio.

### 2.2 DependÃªncias do frontend React
```bash
cd FrontGoDgital
npm install
```
- Copie `FrontGoDgital/.env.example` para `FrontGoDgital/.env` e ajuste a URL da API se estiver usando outro endpoint.

### 2.3 Certificados e perfis HTTPS
- Certificados prÃ©-gerados vivem em `ssl_certificates/` (`server.crt`, `server.key`, `keystore.p12`).
- Para rodar o backend em HTTPS utilize o perfil `https` (`mvn spring-boot:run -Dspring-boot.run.profiles=https`).
- O frontend roda em HTTP por padrÃ£o; configure proxies HTTPS somente se necessÃ¡rio.

---

## 3. InicializaÃ§Ã£o dos serviÃ§os

### 3.1 AI Service (Flask)
```bash
cd ai_module
set USE_HTTPS=false  # Windows PowerShell: $env:USE_HTTPS="false"
python ai_service.py
```
- Porta padrÃ£o em modo desenvolvimento: `5001` (HTTP). Para habilitar HTTPS defina `USE_HTTPS=true`, utilize certificados em `ssl_certificates/` e a porta passarÃ¡ a ser `5443`.
- Endpoints principais: `/predict`, `/health`, `/monitoring`.

### 3.2 Backend Spring Boot
```bash
cd synvia-core
mvn spring-boot:run
```
- Porta padrÃ£o: `8080` (HTTP). Habilite `-Dspring.profiles.active=https` apenas quando precisar de TLS local.
- A URL base da API Ã© `/api`.

### 3.3 Frontend React
```bash
cd FrontGoDgital
npm start
```
- Porta padrÃ£o: `3000`.
- O proxy para o backend estÃ¡ configurado no `package.json` para `http://localhost:8080`.

> Em Windows, os scripts `start_system.bat` e `stop_system.bat` automatizam a orquestraÃ§Ã£o.

---

## 4. PÃ³s-start e validaÃ§Ãµes

### 4.1 Health-checks essenciais
```bash
curl http://localhost:5001/health
curl http://localhost:8080/actuator/health
curl http://localhost:3000 --head
```

### 4.2 Login padrÃ£o
- URL: `http://localhost:3000/login`
- UsuÃ¡rio: `admin@synvia.io`
- Senha: `admin123`

### 4.3 Testes funcionais rÃ¡pidos
- Dashboard de Auditoria (rota `/auditoria`) exibe mÃ©tricas e grÃ¡ficos.
- Portal de Direitos (rota `/portal-direitos`) responde sem autenticaÃ§Ã£o.
- Endpoint `/api/dashboard/auditoria/metricas-gerais` retorna dados em JSON.

---

## 5. FinalizaÃ§Ã£o dos serviÃ§os
- Pressione `Ctrl+C` em cada terminal para desligar processos manuais.
- No Windows, execute `.\stop_system.bat` para encerrar os serviÃ§os iniciados pelo script.
- Limpe caches temporÃ¡rios com `npm cache clean --force` e `mvn clean` quando necessÃ¡rio.

---

## 6. Troubleshooting avanÃ§ado

| CenÃ¡rio | DiagnÃ³stico | AÃ§Ã£o |
| --- | --- | --- |
| Backend nÃ£o sobe | Verifique logs em `synvia-core/target/spring.log` | Confirme versÃ£o do Java e credenciais de banco. |
| Erros CORS | Confira `FrontGoDgital/src/services/api.js` e `synvia-core` -> `WebSecurityConfig` | Alinhe as origens permitidas. |
| IA sem cache | Confirme disponibilidade do Redis (opcional) ou utilize modo fallback | Ajuste `REDIS_URL` ou desabilite temporariamente. |
| HTTPS falha | Certifique-se de que `keystore.p12` estÃ¡ acessÃ­vel e senha correta | Regere certificados com `generate_ssl_certs.sh` se necessÃ¡rio. |

---

## 7. Checklist integrado de validaÃ§Ã£o
```bash
pytest -q                      # Testes rÃ¡pidos do mÃ³dulo de IA
mvn clean verify               # Backend com build + testes
npm run lint && npm test       # Qualidade e testes do frontend
docker compose up -d          # ExecuÃ§Ã£o integrada com chaves LLM de sandbox
```

> Execute os comandos apÃ³s alteraÃ§Ãµes relevantes ou antes de homologaÃ§Ãµes.

## 8. ReferÃªncias
- [InÃ­cio rÃ¡pido](INICIO_RAPIDO.md)
- [DocumentaÃ§Ã£o tÃ©cnica consolidada](../technical/DOCUMENTACAO_TECNICA_COMPLETA.md)
- [Roadmap estratÃ©gico e prÃ³ximos passos](../roadmap/ROADMAP_SYNVIA.md)

> Ãšltima revisÃ£o: outubro/2025


