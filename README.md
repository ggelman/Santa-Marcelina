# Synvia Platform — Onde estrutura encontra fluidez

Synvia é um ecossistema modular que transforma operações complexas em experiências claras. O monorepo reúne:

- **Synvia Front (FrontGoDgital/)**: SPA em React 18 com autenticação JWT, dashboards configuráveis e módulos plugáveis.
- **Synvia Core (synvia-core/)**: Spring Boot 3.5.x para orquestração operacional, segurança e integrações.
- **Synvia Intelligence (i_module/)**: Flask + ML/LLM (Prophet, OpenAI, Gemini) com cache e monitoramento estruturado.

O ambiente local executa **em HTTP por padrão** (3000 / 8080 / 5001), com suporte opcional a HTTPS documentado.

> Estado atual: Front 85% • Core 85% • Intelligence 80% • Infra/DevSecOps 70%  
> Última revisão: outubro/2025

---

## Arquitetura em alto nível
`
Synvia Front (3000) --> Synvia Core API (8080) --> Synvia Intelligence (5001)
           |                 |                         |
           +-----------------+-------------------------+
                     Serviços Compartilhados: MySQL • Redis • Observabilidade
`

---

## Execução rápida (modo HTTP)
1. Copie os templates .env:
   `ash
   cp FrontGoDgital/.env.example FrontGoDgital/.env
   cp ai_module/.env.example ai_module/.env
   `
   Ajuste as variáveis conforme necessário (URLs, credenciais, chaves LLM).
2. Em três terminais diferentes:
   `ash
   # Terminal 1 — IA (porta 5001)
   cd ai_module
   python -m venv .venv && source .venv/bin/activate  # opcional
   pip install -r requirements.txt
   export USE_HTTPS=false  # PowerShell: ="false"
   python ai_service.py

   # Terminal 2 — Core API (porta 8080)
   cd synvia-core
   mvn spring-boot:run

   # Terminal 3 — Frontend (porta 3000)
   cd FrontGoDgital
   npm install
   npm start
   `
3. Acesse http://localhost:3000. Credenciais padrão: dmin@synvia.io / dmin123.
4. Health-checks: http://localhost:8080/actuator/health e http://localhost:5001/health.

> Automatização: execute start_system.bat (PowerShell ou Prompt de Comando) para iniciar os três módulos em HTTP.

Scripts utilitários:
- start_system.bat / stop_system.bat — orquestram/encerram todos os serviços.
- system_status.bat — verifica portas e health checks (3000/8080/5001).
- 	est_sistema_seguranca.bat — smoke tests de conectividade.

---

## Estrutura do repositório
`
FrontGoDgital/          # Synvia Front (React)
synvia-core/            # Synvia Core API (Spring Boot)
ai_module/              # Synvia Intelligence (Flask/ML)
llm-gateway/            # Gateway experimental para orquestração LLM
docs/                   # Documentação oficial (índice em docs/README.md)
ssl_certificates/       # Certificados autoassinados (uso opcional)
start_system.bat        # Bootstrap em HTTP
system_status.bat       # Diagnóstico das portas
`

---

## Documentação essencial
- Índice geral: [docs/README.md](docs/README.md)
- Guias operacionais: [docs/guides/](docs/guides)
- Segurança: [docs/security/](docs/security)
- Referência técnica: [docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md](docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md)
- Roadmap unificado: [docs/roadmap/ROADMAP_SYNVIA.md](docs/roadmap/ROADMAP_SYNVIA.md)

---

## Roadmap resumido
- **Front**: modularizar páginas LGPD, adicionar testes, incluir widget “Synvia Insights”.
- **Core**: MFA/WebAuthn, llm-gateway com mTLS, observabilidade (OpenTelemetry).
- **IA**: atualizar SDKs, orquestrar múltiplos provedores, ampliar testes pytest.
- **Infra**: pipeline CI/CD unificado, scripts multi-OS/Docker compose, gestão de segredos (Vault).

Detalhamento completo em [docs/roadmap/ROADMAP_SYNVIA.md](docs/roadmap/ROADMAP_SYNVIA.md).

---

## Contribuindo
1. Leia os guias em docs/.
2. Crie branches temáticos (eat/, chore/, docs/) com commits semânticos.
3. Execute os testes relevantes (pytest, mvn clean verify, 
pm test).
4. Em PRs, registre impactos e validações — equilíbrio entre estrutura e fluidez é o ritmo Synvia.
