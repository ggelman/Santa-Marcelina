# 🛠️ Documentação Técnica Consolidada
> Sistema goDigital Code — Padaria Santa Marcelina

---

## 1. Arquitetura Geral
```
┌─────────────────────────┐        ┌──────────────────────┐
│ FrontGoDgital (React)   │ <────> │ padariaApi (Spring)  │ <──┐
│ Porta 3000              │        │ Porta 8080 / 8443    │    │
└─────────────────────────┘        └──────────────────────┘    │
            ▲                                 ▲                │
            │                                 │                │
            │                                 │                ▼
            │                                 │        ┌────────────────┐
            │                                 └──────> │ MySQL Database │
            │                                          └────────────────┘
            │
            │        ┌──────────────────────────┐
            └──────> │ ai_module (Flask + ML)   │
                     │ Porta 5443 (HTTPS) / 5001 │
                     └──────────────────────────┘
```
- **Comunicação interna:** HTTP/JSON, com suporte a HTTPS nos serviços Java e Python.
- **Autenticação:** JWT emitido pelo backend e armazenado no frontend.
- **Observabilidade:** logs estruturados e endpoints de health-check expostos por todos os módulos.

---

## 2. Detalhamento por Módulo

### 2.1 FrontGoDgital (React)
- **Stack:** React 18, React Router 6, Styled Components, Radix UI, Axios.
- **Scripts principais:** `npm start`, `npm run start:https`, `npm run build`.
- **Autenticação:** interceptors no `src/services/api.js` adicionam o header `Authorization`.
- **Principais páginas:** `DashboardAuditoria.js`, `PortalDireitosLGPD.js`, fluxos administrativos em `src/pages/`.
- **Build:** `react-scripts` (Webpack 5). O build gera artefatos em `build/`.

### 2.2 padariaApi (Spring Boot)
- **Stack:** Java 17, Spring Boot 3.5.x, Spring Data JPA, Spring Security, JWT, Maven.
- **Configuração padrão:** `application.properties` (HTTP em `8080`).
- **Perfil HTTPS:** `application-https.properties` (porta `8443`, keystore em `ssl_certificates/keystore.p12`).
- **Banco de dados:** MySQL `padaria_santa_marcelina` com `spring.jpa.hibernate.ddl-auto=update`.
- **APIs destaque:** controladores LGPD (`DashboardAuditoriaController`, `ConsentimentoLGPDController`, `SolicitacoesLGPDController`) e autenticação (`AuthController`).
- **Integração com IA:** propriedade `ai.service.url` aponta para o endpoint Flask protegido.

### 2.3 ai_module (Flask + Machine Learning)
- **Stack:** Python 3.10+, Flask, Flask-Limiter, Prophet, pandas, numpy, redis, integrações opcionais com OpenAI/Gemini.
- **Porta padrão:** `5443` (HTTPS com certificados em `ssl_certificates/`). Se `USE_HTTPS=false`, a aplicação utiliza `5001` (HTTP).
- **Arquivos-chave:**
  - `ai_service.py` — API principal e orquestração de modelos.
  - `redis_cache.py` — cache de previsões com TTL configurável.
  - `monitoring_system.py` — métricas e logs estruturados.
- **Variáveis de ambiente úteis:** `USE_HTTPS`, `AI_SERVICE_PORT`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `REDIS_URL`.

---

## 3. Integração e Fluxos

1. **Login e autorização:**
   - Frontend envia credenciais para `/api/auth/login`.
   - Backend autentica, gera JWT e refresh token.
   - Frontend persiste tokens e passa a chamar APIs protegidas com o header `Authorization`.

2. **Solicitações LGPD:**
   - Frontend consome `/api/dashboard/auditoria/*` para métricas.
   - Portal público chama `/api/public/lgpd/solicitacoes/*` sem autenticação.

3. **Predições de IA:**
   - Backend invoca `ai.service.url` para previsões ou insights.
   - AI Service utiliza cache Redis e fallback `fallback_data/` em caso de indisponibilidade.

---

## 4. Configurações Relevantes

| Componente | Arquivo | Observações |
| --- | --- | --- |
| Backend | `application.properties` | Define porta 8080, credenciais MySQL (via variáveis `DB_USERNAME` / `DB_PASSWORD`). |
| Backend | `application-https.properties` | Porta 8443, caminhos do keystore e protocolo TLS 1.2+. |
| Frontend | `package.json` | Scripts `start` (HTTP) e `start:https` (HTTPS via certificados locais). |
| AI Service | `ai_service.py` | Seleciona HTTPS automaticamente e carrega certificados de `../ssl_certificates`. |
| Certificados | `ssl_certificates/` | Inclui `server.crt`, `server.key`, `keystore.p12`; podem ser regenerados via `generate_ssl_certs.sh`. |

---

## 5. Observabilidade e Segurança

- **Health-checks:**
  - `http(s)://localhost:8080/actuator/health`
  - `http(s)://localhost:5443/health`
  - Frontend responde com cabeçalho `200 OK` na rota raiz.
- **Logs:**
  - Backend: console + arquivos configuráveis via Spring Boot.
  - AI Service: logger estruturado com níveis e métricas (ver `monitoring_system.py`).
- **Rate limiting:** habilitado no Flask (`Flask-Limiter`) e disponível no backend via `RateLimitingFilter` (desativado por padrão, ativar com `app.rate-limiting.enabled=true`).
- **Autenticação:** JWT + refresh tokens; tokens configurados em `application.properties` (`jwt.secret`, `jwt.expiration`, `jwt.refresh.*`).

---

## 6. Dados e Persistência

- **MySQL:** utilizado para cadastros, vendas e histórico LGPD. Configuração padrão presume instância local (`localhost:3306`).
- **Fallback data:** pastas `fallback_data/` e `ai_module/fallback_data/` armazenam dados para demonstrações em caso de indisponibilidade externa.
- **Backups:** propriedade `backup.storage.location` define diretório destino. Ajuste para caminhos válidos no ambiente alvo.

---

## 7. Build e Testes

| Módulo | Comando de build | Testes |
| --- | --- | --- |
| Frontend | `npm run build` | `npm test` |
| Backend | `mvn clean install` | `mvn test` |
| AI Service | — | Scripts unitários em `ai_module/test_*.py` |

> Execute os testes após alterações em fluxos críticos e registre novos casos conforme necessário.

---

## 8. Referências Complementares
- [Guia de execução completo](../guides/GUIA_EXECUCAO_COMPLETO.md)
- [Roadmap estratégico e backlog futuro](../ROADMAP_TRANSFORMACAO_DIGITAL.md)
- [Documentação de segurança](../security/SECURITY_ALERTS_DOCUMENTATION.md)

> Última revisão: outubro/2025
