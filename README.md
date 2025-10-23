# Synvia Platform — Onde estrutura encontra fluidez

Synvia é um ecossistema modular que transforma operações complexas em experiências claras. O monorepo reúne:

- **Synvia Front (`FrontGoDgital/`)**: SPA em React 18 com autenticação JWT, dashboards configuráveis e módulos plugáveis.
- **Synvia Core (`synvia-core/`)**: Spring Boot 3.5.x para orquestração operacional, segurança e integrações.
- **Synvia Intelligence (`ai_module/`)**: Flask + ML/LLM (Prophet, OpenAI, Gemini) com cache e monitoramento estruturado.

Ambientes locais agora executam **em HTTP por padrão** (3000 / 8080 / 5001) com suporte opcional a HTTPS documentado.

> Estado atual: Front 85% • Core 85% • Intelligence 80% • Infra/DevSecOps 70%  
> Última revisão: outubro/2025

---

## Arquitetura em alto nível
```
Synvia Front (3000) --> Synvia Core API (8080) --> Synvia Intelligence (5001)
           |                 |                         |
           +-----------------+-------------------------+
                     Serviços Compartilhados: MySQL • Redis • Observabilidade
```

---

## Execução rápida (modo HTTP)
```bash
# Terminal 1 – IA
cd ai_module
python -m venv .venv && source .venv/bin/activate  # opcional
pip install -r requirements.txt
export USE_HTTPS=false  # PowerShell: $env:USE_HTTPS="false"
python ai_service.py      # Porta 5001

# Terminal 2 – Core API
cd synvia-core
mvn spring-boot:run       # Porta 8080

# Terminal 3 – Frontend
cd FrontGoDgital
npm install
npm start                 # Porta 3000
```

Credenciais padrão: `admin@synvia.io` / `admin123`  
Health-checks: `http://localhost:8080/actuator/health` e `http://localhost:5001/health`

Scripts utilitários (Windows):
- `start_system.bat` / `stop_system.bat` — orquestração completa em HTTP
- `system_status.bat` — checagem das portas 3000/8080/5001
- `test_sistema_seguranca.bat` — smoke tests de conectividade

---

## Estrutura do repositório
```
FrontGoDgital/          # Synvia Front (React)
synvia-core/            # Synvia Core API (Spring Boot)
ai_module/              # Synvia Intelligence (Flask/ML)
llm-gateway/            # Gateway experimental para orquestração LLM
docs/                   # Documentação oficial (índice em docs/README.md)
ssl_certificates/       # Certificados autoassinados (uso opcional)
start_system.bat        # Bootstrap em HTTP
system_status.bat       # Diagnóstico das portas
```

Templates de configuração:  
`FrontGoDgital/.env.example` e `ai_module/.env.example` — copie para `.env` localmente e ajuste detalhes (API URL, chaves LLM, credenciais DB).

---

## Documentação essencial
- Índice geral: [`docs/README.md`](docs/README.md)
- Guias operacionais: [`docs/guides/`](docs/guides)
- Segurança: [`docs/security/`](docs/security)
- Referência técnica: [`docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md`](docs/technical/DOCUMENTACAO_TECNICA_COMPLETA.md)
- Roadmap unificado: [`docs/roadmap/ROADMAP_SYNVIA.md`](docs/roadmap/ROADMAP_SYNVIA.md)

---

## Roadmap resumido
- **Front**: modularizar páginas LGPD, adicionar testes, widget Synvia Insights.
- **Core**: MFA/WebAuthn, `llm-gateway` com mTLS, observabilidade OpenTelemetry.
- **IA**: atualizar SDKs, orquestrar múltiplos provedores, ampliar testes `pytest`.
- **Infra**: pipeline CI/CD unificado, scripts multi-OS, gestão de segredos (Vault).

Veja o detalhamento completo e backlog em [`ROADMAP_SYNVIA.md`](docs/roadmap/ROADMAP_SYNVIA.md).

---

## Como contribuir
1. Leia os guias em `docs/`.
2. Crie branches temáticos (`feat/`, `chore/`, `docs/`) com commits semânticos.
3. Execute testes relevantes (`pytest`, `mvn clean verify`, `npm test`).
4. Registre impactos e validações no pull request — equilíbrio entre estrutura e fluidez é a cadência da Synvia.
