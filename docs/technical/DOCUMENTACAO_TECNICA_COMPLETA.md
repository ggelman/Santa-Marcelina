﻿# ðŸ› ï¸ DocumentaÃ§Ã£o TÃ©cnica Consolidada
> Sistema goDigital Code â€” Padaria Santa Marcelina

---

## 1. Arquitetura Geral
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ FrontGoDgital (React)   â”‚ <â”€â”€â”€â”€> â”‚ synvia-core (Spring)  â”‚ <â”€â”€â”
â”‚ Porta 3000              │        │ Porta 8080 (8443 opcional)    â”‚    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â”‚
            â–²                                 â–²                â”‚
            â”‚                                 â”‚                â”‚
            â”‚                                 â”‚                â–¼
            â”‚                                 â”‚        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
            â”‚                                 â””â”€â”€â”€â”€â”€â”€> â”‚ MySQL Database â”‚
            â”‚                                          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
            â”‚
            â”‚        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
            â””â”€â”€â”€â”€â”€â”€> â”‚ ai_module (Flask + ML)   â”‚
                     â”‚ Porta 5443 (HTTPS) / 5001 â”‚
                     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```
- **ComunicaÃ§Ã£o interna:** HTTP/JSON, com suporte a HTTPS nos serviÃ§os Java e Python.
- **AutenticaÃ§Ã£o:** JWT emitido pelo backend e armazenado no frontend.
- **Observabilidade:** logs estruturados e endpoints de health-check expostos por todos os mÃ³dulos.

---

## 2. Detalhamento por MÃ³dulo

### 2.1 FrontGoDgital (React)
- **Stack:** React 18, React Router 6, Styled Components, Radix UI, Axios.
- **Scripts principais:** `npm start`, `npm run start:https`, `npm run build`.
- **AutenticaÃ§Ã£o:** interceptors no `src/services/api.js` adicionam o header `Authorization`.
- **Principais pÃ¡ginas:** `DashboardAuditoria.js`, `PortalDireitosLGPD.js`, fluxos administrativos em `src/pages/`.
- **Build:** `react-scripts` (Webpack 5). O build gera artefatos em `build/`.
- **PrÃ³ximos ajustes (0-3 meses):** centralizar requisiÃ§Ãµes no `api.js` parametrizado via variÃ¡veis seguras, modularizar pÃ¡ginas extensas com hooks/componentes reutilizÃ¡veis, instrumentar telemetria (Web Vitals + OpenTelemetry) e embarcar widget Gemini para insights rÃ¡pidos.

### 2.2 synvia-core (Spring Boot)
- **Stack:** Java 17, Spring Boot 3.5.x, Spring Data JPA, Spring Security, JWT, Maven.
- **ConfiguraÃ§Ã£o padrÃ£o:** `application.properties` (HTTP em `8080`).
- **Perfil HTTPS:** `application-https.properties` (porta `8443`, keystore em `ssl_certificates/keystore.p12`).
- **Banco de dados:** MySQL `padaria_santa_marcelina` com `spring.jpa.hibernate.ddl-auto=update`.
- **APIs destaque:** controladores LGPD (`DashboardAuditoriaController`, `ConsentimentoLGPDController`, `SolicitacoesLGPDController`) e autenticaÃ§Ã£o (`AuthController`).
- **IntegraÃ§Ã£o com IA:** propriedade `ai.service.url` aponta para o endpoint Flask protegido.
- **PrÃ³ximos ajustes (0-3 meses):** criar microserviÃ§o `llm-gateway` com mTLS e fila de prompts, ativar MFA/WebAuthn, rotacionar refresh tokens, aplicar cache/ETag em endpoints pÃºblicos e ampliar tracing distribuÃ­do.

### 2.3 ai_module (Flask + Machine Learning)
- **Stack:** Python 3.10+, Flask, Flask-Limiter, Prophet, pandas, numpy, redis, integraÃ§Ãµes opcionais com OpenAI/Gemini.
- **Porta padrÃ£o:** `5443` (HTTPS com certificados em `ssl_certificates/`). Se `USE_HTTPS=false`, a aplicaÃ§Ã£o utiliza `5001` (HTTP).
- **Arquivos-chave:**
  - `ai_service.py` â€” API principal e orquestraÃ§Ã£o de modelos.
  - `redis_cache.py` â€” cache de previsÃµes com TTL configurÃ¡vel.
  - `monitoring_system.py` â€” mÃ©tricas e logs estruturados.
- **VariÃ¡veis de ambiente Ãºteis:** `USE_HTTPS`, `AI_SERVICE_PORT`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `REDIS_URL`.
- **PrÃ³ximos ajustes (0-3 meses):** atualizar SDKs (OpenAI/Gemini), implementar orquestrador multi-provedor com enriquecimento de contexto multivariado, liberar respostas multimodais, versionar pipelines com MLflow/DVC e registrar mÃ©tricas comparativas.

---

## 3. IntegraÃ§Ã£o e Fluxos

1. **Login e autorizaÃ§Ã£o:**
   - Frontend envia credenciais para `/api/auth/login`.
   - Backend autentica, gera JWT e refresh token.
   - Frontend persiste tokens e passa a chamar APIs protegidas com o header `Authorization`.

2. **SolicitaÃ§Ãµes LGPD:**
   - Frontend consome `/api/dashboard/auditoria/*` para mÃ©tricas.
   - Portal pÃºblico chama `/api/public/lgpd/solicitacoes/*` sem autenticaÃ§Ã£o.

3. **PrediÃ§Ãµes de IA:**
   - Backend invoca `ai.service.url` para previsÃµes ou insights.
   - AI Service utiliza cache Redis e fallback `fallback_data/` em caso de indisponibilidade.

---

## 4. ConfiguraÃ§Ãµes Relevantes

| Componente | Arquivo | ObservaÃ§Ãµes |
| --- | --- | --- |
| Backend | `application.properties` | Define porta 8080, credenciais MySQL (via variÃ¡veis `DB_USERNAME` / `DB_PASSWORD`). |
| Backend | `application-https.properties` | Porta 8443 (opcional), caminhos do keystore e protocolo TLS 1.2+. |
| Frontend | `package.json` | Scripts `start` (HTTP) e `start:https` (HTTPS via certificados locais). |
| AI Service | `ai_service.py` | Seleciona HTTPS automaticamente e carrega certificados de `../ssl_certificates`. |
| Certificados | `ssl_certificates/` | Inclui `server.crt`, `server.key`, `keystore.p12`; podem ser regenerados via `generate_ssl_certs.sh`. |

---

## 5. Observabilidade e SeguranÃ§a

- **Health-checks:**
  - `http(s)://localhost:8080/actuator/health`
  - `http(s)://localhost:5443/health`
  - Frontend responde com cabeÃ§alho `200 OK` na rota raiz.
- **Logs:**
  - Backend: console + arquivos configurÃ¡veis via Spring Boot.
  - AI Service: logger estruturado com nÃ­veis e mÃ©tricas (ver `monitoring_system.py`).
- **Rate limiting:** habilitado no Flask (`Flask-Limiter`) e disponÃ­vel no backend via `RateLimitingFilter` (desativado por padrÃ£o, ativar com `app.rate-limiting.enabled=true`).
- **Telemetria planejada:** adoÃ§Ã£o de OpenTelemetry para rastreamento distribuÃ­do (frontend â†’ backend â†’ IA) e exposiÃ§Ã£o de mÃ©tricas tÃ©cnicas para integraÃ§Ã£o com SIEM/SRE.
- **AutenticaÃ§Ã£o:** JWT + refresh tokens; tokens configurados em `application.properties` (`jwt.secret`, `jwt.expiration`, `jwt.refresh.*`).

---

## 6. Dados e PersistÃªncia

- **MySQL:** utilizado para cadastros, vendas e histÃ³rico LGPD. ConfiguraÃ§Ã£o padrÃ£o presume instÃ¢ncia local (`localhost:3306`).
- **Fallback data:** pastas `fallback_data/` e `ai_module/fallback_data/` armazenam dados para demonstraÃ§Ãµes em caso de indisponibilidade externa.
- **Backups:** propriedade `backup.storage.location` define diretÃ³rio destino. Ajuste para caminhos vÃ¡lidos no ambiente alvo.

---

## 7. Build e Testes

| MÃ³dulo | Comando de build | Testes |
| --- | --- | --- |
| Frontend | `npm run build` | `npm test` |
| Backend | `mvn clean install` | `mvn test` |
| AI Service | â€” | Scripts unitÃ¡rios em `ai_module/test_*.py` |

> Execute os testes apÃ³s alteraÃ§Ãµes em fluxos crÃ­ticos e registre novos casos conforme necessÃ¡rio.

---

## 8. Backlog tÃ©cnico priorizado (0-3 meses)
- **SeguranÃ§a e acesso:** MFA/WebAuthn, rotaÃ§Ã£o de refresh tokens, centralizaÃ§Ã£o de segredos e hardening de pipelines CI/CD.
- **Observabilidade:** instrumentar tracing e mÃ©tricas (OpenTelemetry), habilitar SIEM integrado e dashboards estatÃ­sticos.
- **IA e dados:** router multi-provedor (Gemini + OpenAI), versionamento MLflow/DVC, pipeline estatÃ­stico de correlaÃ§Ã£o/regressÃ£o.
- **Frontend:** modularizaÃ§Ã£o, centralizaÃ§Ã£o de chamadas no `api.js` e widget Gemini para insights.
- **Blockchain:** validar orÃ§amento/parceiros e preparar PoC permissionada com auditoria LGPD.

## 9. ReferÃªncias Complementares
- [Guia de execuÃ§Ã£o completo](../guides/GUIA_EXECUCAO_COMPLETO.md)
- [DocumentaÃ§Ã£o de seguranÃ§a](../security/SECURITY_ALERTS_DOCUMENTATION.md)

> Ãšltima revisÃ£o: outubro/2025

