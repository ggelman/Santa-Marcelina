# Synvia Platform — Onde estrutura encontra fluidez.

Synvia é o ecossistema modular que transforma operações complexas em experiências claras. O monorepo integra fronteira de design e engenharia: um frontend React responsivo, o núcleo Spring Boot de orquestração operacional e o serviço de inteligência em Flask que traduz dados brutos em decisões. Cada módulo se adapta a diferentes verticais — varejo, serviços, saúde, educação — preservando a fluidez da marca.

> **Estado atual:** Synvia Front 85 % • Synvia Core API 85 % • Synvia Intelligence 80 % • Infra/DevSecOps 70 %  
> **Última revisão:** outubro/2025

---

## Visão arquitetural
```
Synvia Front (React)  -->  Synvia Core API (Spring Boot)  -->  Synvia Intelligence (Flask/ML)
         |                         |                                  |
         +-------------------------+----------------------------------+
                          Shared Services: MySQL • Redis • Observabilidade
```
- **Synvia Front (`FrontGoDgital/`)**: experiência single-page em React 18 com autenticação JWT, dashboards configuráveis e módulos plugáveis (compliance, operações, atendimento).
- **Synvia Core API (`synvia-core/`)**: Spring Boot 3.5.x com segurança avançada, automação de processos, integrações com o motor de IA e suporte multi-tenant planejado.
- **Synvia Intelligence (`ai_module/`)**: serviço Flask com Prophet/LLM, camada de cache Redis e monitoramento estruturado para insights preditivos e prescritivos.
- **Infraestrutura compartilhada**: certificados em `ssl_certificates/`, scripts de orquestração em Windows e documentação viva em `docs/`.

---

## Manifesto Synvia aplicado ao produto
- **Propósito**: transformar complexidade em clareza. Cada módulo nasce modular, adaptável e inteligente.
- **Missão**: desenhar tecnologias que se moldam às pessoas — componentes configuráveis por segmento, sem perder precisão.
- **Visão**: referência em design inteligente; APIs silenciosas, experiências claras, dados que respiram em tempo real.
- **Promessa**: estrutura com leveza. Estabilidade arquitetural com pipelines que evoluem sem atrito.
- **Personalidade**: inovadora, sofisticada, fluida, confiável e acessível. Voz precisa e calma: falar apenas o necessário.
- **Tagline**: **Onde estrutura encontra fluidez.**

---

## Como executar rapidamente
1. Garanta Java 21, Node.js 18, Python 3.10+ e uma instância MySQL local.
2. Opcional: ajuste variáveis de ambiente para adequar endpoints (por exemplo `REACT_APP_API_BASE_URL`, `AI_SERVICE_URL`).
3. Inicie os módulos:
   ```bash
   # Synvia Intelligence
   cd ai_module
   pip install -r requirements.txt
   python ai_service.py

   # Synvia Core API
   cd synvia-core
   mvn spring-boot:run

   # Synvia Front
   cd FrontGoDgital
   npm install
   npm start
   ```
4. Acesse `http://localhost:3000`. Usuário padrão atual: `admin@padaria.com` / `admin123` (será evoluído para credenciais Synvia em sprint dedicada).
5. Health-checks essenciais: `http://localhost:8080/actuator/health` (Core API) e `http://localhost:5001/api/ai/health` (Intelligence).

> Revisite o [guia rápido](docs/guides/INICIO_RAPIDO.md) e o [guia completo](docs/guides/GUIA_EXECUCAO_COMPLETO.md) para cenários avançados.

---

## Capacidades principais
- **Governança de dados**: fluxos LGPD, consentimento granular e trilhas de auditoria estruturadas.
- **Operações inteligentes**: previsões, insights narrativos LLM e KPIs moduláveis por vertical.
- **Experiência modulável**: layout, widgets e integrações plugáveis via configuração.
- **Segurança e observabilidade**: rate limiting, refresh tokens, monitoramento estruturado, export OTLP.

---

## Estrutura do repositório
```
FrontGoDgital/          # Synvia Front (React)
synvia-core/            # Synvia Core API (Spring Boot)
ai_module/              # Synvia Intelligence (Flask/ML)
llm-gateway/            # Gateway experimental para orquestração LLM
docs/                   # Documentação oficial
ssl_certificates/       # Certificados autoassinados
start_system.bat        # Bootstrap rápido (Windows)
system_status.bat       # Diagnóstico rápido (Windows)
```

---

## Documentação essencial
- Índice vivo: [`docs/README.md`](docs/README.md)
- Guias de execução: [`docs/guides/`](docs/guides)
- Segurança e compliance: [`docs/security/`](docs/security)
- Referência técnica: [`docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md`](docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md)
- Roadmap estratégico: [`docs/ROADMAP_TRANSFORMACAO_DIGITAL.md`](docs/ROADMAP_TRANSFORMACAO_DIGITAL.md)

---

## Status atual e próximos incrementos

| Domínio | Status | Próxima evolução Synvia |
| --- | --- | --- |
| Synvia Front | 85 % | Design system Synvia (paleta Space Cadet/Snow/Steel Blue), componentes moduláveis, roteamento multi-tenant |
| Synvia Core API | 85 % | Separação de domínios (Core, Compliance, Commerce), MFA/WebAuthn, mTLS com `llm-gateway` |
| Synvia Intelligence | 80 % | Orquestrador multi-LLM, MLflow/DVC, enriquecimento contextual por vertical |
| Infra & DevSecOps | 70 % | IaC, CI/CD observável, adaptação para nuvem híbrida |

---

## Roadmap imediato
- Renomear domínios e artefatos (classes, pacotes, assets) para Synvia.
- Externalizar credenciais e parâmetros de negócio em camadas de configuração.
- Construir kit de identidade (logos, cores, tipografia) no frontend.
- Evoluir scripts de start para suportar Linux/macOS e pipelines automatizados.
- Conectar `llm-gateway` como camada oficial de inteligência conversacional.

---

## Validação rápida
```bash
pytest -q                      # Synvia Intelligence
mvn clean verify               # Synvia Core API
npm run lint && npm test       # Synvia Front
docker compose up -d           # Execução integrada (após configurar variáveis LLM)
```

---

## Contribuição
1. Leia os guias em `docs/` e alinhe entregas ao manifesto Synvia.
2. Use branches temáticos (`feat/`, `chore/`, `docs/`) e convenções de commit semânticas.
3. Execute os testes relevantes e anexe evidências nos PRs.
4. Descreva como a mudança mantém o equilíbrio estrutura × fluidez.

---

## Contato
- Time Synvia: abra issues no repositório ou use os canais internos apontados na documentação.
- Incidentes críticos: siga `docs/security/SECURITY_ALERTS_DOCUMENTATION.md` e o fluxo de resposta dedicado.
