# 🏗️ goDigital Code — Padaria Santa Marcelina

Plataforma integrada de conformidade LGPD e operação digital. O monorepo agrega frontend React, backend Spring Boot e módulo de IA em Flask para entregar monitoramento de auditoria, portal de direitos do titular e previsões de demanda.

> **Status atual:** Frontend 85% • Backend 85% • Módulo de IA 80% • Infra/DevSecOps 70% • **Última atualização:** dezembro/2025

---

## 🌐 Visão arquitetural
```
Frontend (React) ⇄ Backend (Spring Boot) ⇄ IA/ML Service (Flask)
          │                 │
          └────> MySQL + cache e trilhas de auditoria
```
- **Frontend (`FrontGoDgital/`)**: SPA em React 18 com autenticação JWT, dashboards LGPD e portal público para titulares.
- **Backend (`padariaApi/`)**: Spring Boot 3.5.x com APIs LGPD, rate limiting opcional, integrações com IA e MySQL.
- **Módulo de IA (`ai_module/`)**: Flask + Prophet/ML, cache Redis e monitoramento estruturado.
- **Infraestrutura**: certificados SSL em `ssl_certificates/`, scripts `start_system.bat`/`stop_system.bat` e dados de fallback.

---

## 🚀 Como executar rapidamente
1. Configure Java 17+, Node.js 18+, Python 3.10+ e MySQL local.
2. Execute `start_system.bat` (Windows) ou inicie manualmente cada módulo:
   ```bash
   # AI Service
   cd ai_module && pip install -r requirements.txt && python ai_service.py

   # Backend
   cd padariaApi && mvn spring-boot:run

   # Frontend
   cd FrontGoDgital && npm install && npm start
   ```
3. Acesse `http://localhost:3000` (login padrão `admin@padaria.com` / `admin123`).
4. Verifique health-checks: backend (`http://localhost:8080/actuator/health`) e IA (`https://localhost:5443/health`).

> Consulte o [guia de início rápido](docs/guides/INICIO_RAPIDO.md) para detalhes e soluções rápidas.

---

## 🔑 Funcionalidades principais
- Dashboard de auditoria LGPD com métricas, gráficos e alertas em tempo real.
- Portal de direitos do titular público e rastreável.
- Gestão de consentimentos com histórico completo e revogação granular.
- Previsões de demanda e insights de IA com cache resiliente.
- Monitoramento de segurança, logs detalhados e autenticação JWT + refresh tokens.

---

## 🗂️ Estrutura essencial do repositório
```
├── FrontGoDgital/         # Frontend React
├── padariaApi/            # Backend Spring Boot
├── ai_module/             # Serviço de IA/ML em Flask
├── docs/                  # Documentação oficial revisada
├── ssl_certificates/      # Certificados autoassinados
├── start_system.bat       # Orquestração (Windows)
└── system_status.bat      # Diagnóstico rápido (Windows)
```

---

## 📚 Documentação centralizada
- Índice geral: [`docs/README.md`](docs/README.md)
- Guias de execução: [`docs/guides/`](docs/guides)
- Segurança: [`docs/security/`](docs/security)
- Referência técnica: [`docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md`](docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md)
- Planejamento estratégico: [`docs/ROADMAP_TRANSFORMACAO_DIGITAL.md`](docs/ROADMAP_TRANSFORMACAO_DIGITAL.md)

---

## 📊 Visão consolidada

| Domínio | Status | Ajustes priorizados |
| --- | --- | --- |
| Frontend (React) | 85% operacional | Modularização de telas extensas, hooks compartilhados, widget Gemini e centralização das requisições no `api.js` com variáveis seguras. |
| Backend (Spring Boot) | 85% operacional | Microserviço `llm-gateway` com mTLS, fila de prompts, MFA/WebAuthn, rotação de refresh tokens e cache/ETag para rotas públicas. |
| Módulo de IA (Flask + LLMs) | 80% operacional | Router multi-provedor (Gemini + OpenAI), contexto multivariado, respostas multimodais e versionamento de pipelines com MLflow/DVC. |
| Infra & DevSecOps | 70% parcial | Infra-as-Code, CI/CD unificado com scans, cofre de segredos e trilha blockchain para auditoria LGPD. |

## 🎯 Prioridades imediatas
- Homologar documentação revisada (roadmap, guias, status consolidado).
- Priorização do backlog da Fase 7: MFA administrativo, SIEM integrado e pipelines estatísticos/científicos de dados.
- Validação de orçamento e parceiros para blockchain permissionada.
- Preparação do pacote de evidências executivas e de mercado.

## 🩺 Diagnóstico funcional & mitigação
- **IA:** SDK OpenAI desatualizado e fallback Gemini sem testes integrados → atualizar SDKs, cobrir com testes de integração e registrar métricas comparativas.
- **Backend:** falta telemetria detalhada e caching em endpoints públicos → instrumentar tracing distribuído, aplicar cache/ETag e revisar logs.
- **Frontend:** risco de mixed content e interceptors sem tratamento para expiração simultânea de tokens → padronizar interceptors, reforçar políticas HTTPS e tratativas de sessão.
- **Plataforma:** scripts dependem de Windows e monitoramento distribuído manual → padronizar automações multi-OS e incorporar observabilidade em pipelines.

## 🧪 Checklist de validação rápida
```bash
pytest -q                      # Módulo de IA
mvn clean verify               # Backend
npm run lint && npm test       # Frontend
docker compose up -d          # Execução integrada com chaves LLM de sandbox
```

## 🔄 Trabalho paralelizável
- Atualização de SDKs LLM e implementação do orquestrador (times de IA + DevSecOps).
- Refatoração do consumo de APIs e modularização do frontend.
- Instrumentação de observabilidade distribuída no backend.
- Planejamento da PoC de blockchain permissionada e conformidade.
- Construção do pipeline estatístico (correlação/regressão) para analytics.

---

## 🛣️ Próximas fases
- Hardening de segurança (MFA, SIEM, backups versionados).
- Pipeline estatístico com correlação/regressão nas métricas de negócio.
- Piloto de Blockchain e Smart Contracts para registros de auditoria.
- Evolução para oferta SaaS e multi-tenant.

Os detalhes completos e prioridades estão documentados no [roadmap estratégico](docs/ROADMAP_TRANSFORMACAO_DIGITAL.md).

---

## 🤝 Contribuição
1. Leia os guias em `docs/` antes de iniciar.
2. Crie branches temáticos e siga convenções de commit (`feat:`, `fix:`, `docs:` etc.).
3. Execute testes relevantes (`mvn test`, `npm test`, scripts em `ai_module/test_*.py`).
4. Abra Pull Requests com descrição clara, evidências e checklist de testes.

---

## 📬 Contato
- Equipe goDigital Code — disponível via issues ou canais internos da FIAP.
- Para dúvidas urgentes, consulte `docs/security/SECURITY_ALERTS_DOCUMENTATION.md` e `docs/guides/GUIA_EXECUCAO_COMPLETO.md`.
