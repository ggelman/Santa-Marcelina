# 🗺️ Roadmap Estratégico de Transformação Digital
> goDigital Code — Padaria Santa Marcelina

## 0. Contexto
Com a maturidade em LGPD e Governança de TI atingida, o foco agora é posicionar o goDigital Code como plataforma de mercado. O roadmap abaixo consolida o estado atual do projeto e direciona as evoluções necessárias para incorporar Blockchain, Smart Contracts, estatística aplicada e práticas avançadas de segurança.

---

## 1. Status Consolidado da Implementação

| Módulo | Situação | Destaques atuais | Próximos ajustes |
| --- | --- | --- | --- |
| FrontGoDgital (React) | 85% — operacional | Dashboard de auditoria, Portal de Direitos, módulos administrativos. | Modularizar páginas extensas via hooks/componentes, centralizar requisições no `api.js` com variáveis seguras e habilitar telemetria (Web Vitals + OpenTelemetry). |
| padariaApi (Spring Boot) | 85% — operacional | APIs LGPD, autenticação JWT, integração IA. | Criar microserviço `llm-gateway` com mTLS e fila de prompts, ativar MFA/WebAuthn e rotação de refresh tokens, além de cache/ETag em endpoints públicos. |
| ai_module (Flask/ML) | 80% — operacional | Previsões de demanda, monitoramento estruturado, cache Redis. | Atualizar SDKs (OpenAI/Gemini), construir orquestrador multi-provedor, enriquecer contexto com dados multivariados e versionar pipelines com MLflow/DVC. |
| Infraestrutura & DevSecOps | 70% — parcial | Certificados SSL, scripts de orquestração, logging básico. | Adotar IaC (Terraform/Ansible), unificar CI/CD com testes + scans, centralizar segredos (Vault/Secrets Manager) e amarrar auditoria blockchain à conformidade. |

---

### 1.1 Prioridades imediatas
- Homologar documentação revisada (roadmap, guias, status consolidado).
- Priorizar backlog técnico da Fase 7: MFA administrativo, SIEM integrado e pipelines estatísticos/científicos de dados.
- Validar orçamento e parceiros para blockchain permissionada.
- Preparar pacote de evidências executivas e de mercado.

### 1.2 Plano operacional por domínio

#### Módulo de IA (Gemini + OpenAI)
- **Objetivos:** router multi-provedor, contexto multivariado, respostas multimodais, pipelines versionados e governança reforçada (vault de prompts, auditoria LGPD via blockchain).
- **Entregas priorizadas:**
  - **0-1 mês:** atualizar SDKs OpenAI/Gemini e revisar testes de integração/fallback.
  - **1-2 meses:** implementar orquestrador multi-provedor com balanceamento e métricas comparativas.
  - **2-3 meses:** publicar insights multimodais com registro na trilha blockchain.

#### Frontend (React)
- Centralizar requisições no `src/services/api.js`, parametrizando endpoints via variáveis seguras.
- Instrumentar telemetria (Web Vitals + OpenTelemetry) e modularizar páginas extensas por meio de hooks/componentes reutilizáveis.
- Integrar widget Gemini para insights rápidos e evitar mixed content com políticas HTTPS consistentes.

#### Backend (Spring Boot)
- Criar microserviço `llm-gateway` com mTLS, fila de prompts e observabilidade distribuída.
- Entregar MFA/WebAuthn, rotação de refresh tokens e aplicar cache/ETag em endpoints públicos.
- Ampliar tracing com OpenTelemetry e preparar auditoria blockchain-ready.

#### Plataforma (Infra/DevSecOps)
- Adotar IaC (Terraform/Ansible) e CI/CD unificado com testes, segurança (SAST/DAST) e observabilidade.
- Centralizar segredos em Vault/Secrets Manager, automatizar backups e preparar o programa de conformidade ISO/SOC com lastro blockchain.
- Planejar PoC de blockchain permissionada (Hyperledger Besu/Quorum) alinhada ao orçamento aprovado.

### 1.3 Diagnóstico funcional & mitigação

| Área | Achado | Mitigação planejada |
| --- | --- | --- |
| IA | SDK OpenAI desatualizado e fallback Gemini sem testes de integração | Atualizar dependências, criar suíte de integração multi-provedor e registrar métricas comparativas (latência/custo/qualidade). |
| Backend | Ausência de telemetria detalhada e caching nos endpoints públicos | Instrumentar tracing distribuído, habilitar métricas técnicas e aplicar cache/ETag onde cabível. |
| Frontend | Risco de mixed content e interceptors sem handling de expiração simultânea | Centralizar interceptors com renovação sincronizada de tokens e reforçar políticas HTTPS nos ambientes. |
| Plataforma | Scripts Windows-only e monitoramento distribuído manual | Portar automações para shell multi-OS, incluir execução via Docker Compose e consolidar observabilidade no pipeline. |

### 1.4 Trabalho paralelizável
- Atualização de SDKs LLM + implementação do orquestrador (times de IA e DevSecOps).
- Refatoração do consumo de APIs no frontend (time Front).
- Instrumentação de observabilidade e caching no backend (time Backend).
- Planejamento e orçamento da PoC blockchain (time Plataforma).
- Pipeline estatístico de correlação/regressão (Data/Analytics).

### 1.5 Checklist integrado de validação
```bash
pytest -q                      # IA
mvn clean verify               # Backend Spring Boot
npm run lint && npm test       # Frontend React
docker compose up -d          # Execução integrada com chaves LLM de sandbox
```

---

## 2. Parte 1 — Revisão do Backlog e Sistemas Departamentais

### 2.1 Sistemas de Informação Departamentais (SID) e potencialização
| Área | SID existente/potencial | Como potencializa o goDigital Code |
| --- | --- | --- |
| Finanças | ERP financeiro + conciliação automática | Alimenta indicadores de margem, fluxo de caixa e integra com relatórios LGPD de faturamento. |
| Operações | Sistema de estoque integrado a IoT (sensores) | Atualiza previsões da IA com dados de produção em tempo real, reduzindo rupturas. |
| Marketing & Vendas | CRM omnichannel | Sincroniza consentimentos LGPD, campanhas personalizadas e histórico de interações. |
| Recursos Humanos | HRIS com trilha de treinamento | Controla acessos privilegiados, registra reciclagens de LGPD e incidentes de segurança. |
| Jurídico & Compliance | GRC platform (Governança, Riscos e Compliance) | Consolida evidências de auditoria, contratos e prazos de atendimento aos titulares. |

### 2.2 Funcionalidades x Áreas impactadas
| Funcionalidade | Área(s) beneficiada(s) | Benefícios diretos |
| --- | --- | --- |
| Dashboard de Auditoria LGPD | Compliance, Diretoria | Transparência sobre incidentes e SLAs de atendimento. |
| Portal de Direitos do Titular | Marketing, Jurídico | Reduz esforço manual e garante prazos legais. |
| Previsão de Demanda | Operações, Finanças | Ajusta produção e compras com base em sazonalidade. |
| Sistema de Consentimentos | Marketing, TI | Segmentação responsável de campanhas e trilhas de auditoria. |
| Monitoramento de Segurança | TI, RH | Alertas proativos e evidências para reciclagens obrigatórias. |

### 2.3 Quadro de eficiência organizacional
| Processo | Ganhos de produtividade esperados | Indicadores monitorados |
| --- | --- | --- |
| Atendimento às solicitações LGPD | Redução de 60% no tempo médio de resposta | SLA de atendimento (<15 dias), índice de satisfação do titular. |
| Planejamento de produção | Ajuste dinâmico de lotes e insumos | MAPE das previsões, giro de estoque, desperdício (%). |
| Campanhas de marketing | Personalização conforme consentimento | Taxa de conversão, churn, score de consentimento ativo. |
| Auditoria interna | Evidências centralizadas e rastreáveis | Número de não conformidades, tempo para fechamento de auditoria. |
| Gestão de acessos | Revisões periódicas automatizadas | % de acessos revistos no prazo, incidentes de privilégio indevido. |

---

## 3. Parte 2 — Segurança e Tríade CIA

### 3.1 Políticas técnicas propostas
- **Confidencialidade:** autenticação multifator para perfis administrativos, criptografia TLS ponta a ponta, criptografia em repouso para backups sensíveis.
- **Integridade:** versionamento de logs com hashing (SHA-256), validação de payloads via JSON Schema e assinaturas digitais nas respostas críticas.
- **Disponibilidade:** clusterização opcional do backend, readiness probes para AI Service, políticas de backup incremental diário + full semanal.
- **Autenticação e Acesso:** RBAC centralizado, revisão trimestral de perfis, integração com diretório corporativo (LDAP/AD) opcional.
- **Backups:** armazenar snapshots MySQL em storage imutável (Object Storage com versionamento) e testar restaurações trimestralmente.

### 3.2 Simulação de ataque
**Cenário:** invasor obtém credenciais expostas de um colaborador e tenta extrair dados pessoais em massa.

**Resposta planejada:**
1. **Detecção:** Rate limiting identifica volume anômalo → alerta em painel de segurança.
2. **Contenção:** política de bloqueio automático do token + IP temporário; autenticação multifator exigida para nova sessão.
3. **Erradicação:** revisão de logs assinados, bloqueio do usuário no AD/Identity Provider, reset de senhas.
4. **Recuperação:** restauração de dados caso haja alteração indevida usando backups incrementais; geração de relatório LGPD para autoridade.
5. **Lições aprendidas:** ajuste de regras de detecção (correlação com IA), reforço de treinamento de engenharia social via HRIS.

---

## 4. Parte 3 — Estatística Aplicada e Tomada de Decisão

1. **Bases de dados:** vendas históricas, cadastros de consentimento, métricas de portal LGPD e logs de auditoria.
2. **Correlação:**
   - Correlação de Pearson entre campanhas ativas e aumento de solicitações LGPD.
   - Correlação Spearman entre indicadores de estoque e previsões de demanda.
3. **Regressão:**
   - Regressão múltipla para prever faturamento considerando variáveis (clima, promoções, consentimento ativo).
   - Regressão logística para estimar probabilidade de incidentes de segurança com base em acessos privilegiados.
4. **Decisões orientadas a dados:**
   - Ajustar plano de produção semanal conforme intervalo de confiança das previsões.
   - Priorizar treinamentos de segurança em áreas com maior propensão a incidentes.
   - Medir impacto de novas funcionalidades no tempo de atendimento LGPD.
5. **Ferramentas:** Python (pandas, statsmodels, scikit-learn), dashboards no frontend com gráficos comparativos e alertas estatísticos (ex.: desvio padrão acima do limite).

---

## 5. Parte 4 — Blockchain e Smart Contracts

### 5.1 Casos de uso propostos
- **Registro imutável de auditorias LGPD:** cada atendimento gera um hash enviado para blockchain permissionada, garantindo rastreabilidade.
- **Token de acesso temporário:** smart contract gerencia tokens de acesso a dados sensíveis, com expiração automática e consentimento explícito.
- **Compliance Financeiro:** registro de conciliações e previsões críticas, fornecendo trilha confiável para parceiros e autoridades.

### 5.2 Protótipo de Smart Contract (Solidity)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract LGPDAuditRegistry {
    struct AuditEvent {
        string protocolo;      // ID interno da solicitação
        string hashRegistro;   // Hash SHA-256 dos dados auditados
        uint256 timestamp;     // Registro em blockchain
        string responsavel;    // Identificador do operador
    }

    mapping(bytes32 => AuditEvent) public eventos;
    event AuditLogged(bytes32 indexed id, string protocolo, string hashRegistro, string responsavel);

    function registrarEvento(
        string memory protocolo,
        string memory hashRegistro,
        string memory responsavel
    ) public {
        bytes32 id = keccak256(abi.encodePacked(protocolo, hashRegistro, block.timestamp));
        eventos[id] = AuditEvent(protocolo, hashRegistro, block.timestamp, responsavel);
        emit AuditLogged(id, protocolo, hashRegistro, responsavel);
    }
}
```
- Deploy inicial sugerido em rede permissionada (Hyperledger Besu ou Quorum).
- Backend assina as transações utilizando carteira de serviço; hash gerado a partir do payload da solicitação.

### 5.3 Integração planejada
1. Serviço Spring Boot cria hash dos dados auditados.
2. Chamada para microserviço blockchain (ou web3 provider) registra o evento.
3. ID do registro blockchain é retornado ao frontend e anexado ao histórico do titular.
4. Rotina diária consolida hashes e verifica integridade comparando com a base local.

---

## 6. Fases de Implementação

| Fase | Horizonte | Entregas principais |
| --- | --- | --- |
| **Fase 7 — Hardening e Observabilidade** | 0-3 meses | MFA administrativo, SIEM integrado, dashboard de estatísticas com correlação, automatização de backups. |
| **Fase 8 — Blockchain Piloto** | 3-6 meses | Microserviço web3, smart contract de auditoria, integração com fluxos LGPD e geração de relatórios imutáveis. |
| **Fase 9 — IA Avançada & Automação** | 6-9 meses | Pipeline MLOps, regressões em produção, recomendações prescritivas para operações e marketing. |
| **Fase 10 — Oferta como Plataforma (SaaS)** | 9-12 meses | Multi-tenant, billing, marketplace de integrações e certificações de segurança (ISO 27001, SOC 2). |

---

## 7. Indicadores de Sucesso
- ≥ 95% de solicitações LGPD respondidas dentro do SLA.
- Redução de 20% no desperdício de insumos via previsões integradas.
- 0 incidentes críticos sem resposta em menos de 1 hora.
- 100% dos eventos críticos registrados na blockchain piloto.
- Aprovação do comitê de governança para lançamento comercial.

---

### Próximos passos imediatos
1. Homologar as atualizações de documentação (este roadmap e guias revisados).
2. Priorizar backlog técnico para fase 7 (MFA, SIEM, pipelines de dados).
3. Validar orçamento e parceiros para implementação blockchain permissionada.
4. Preparar evidências para apresentação executiva e de mercado.

---

## 8. Revolução do Módulo de IA (Gemini + OpenAI)

### 8.1 Orquestração avançada de LLMs
| Iniciativa | Descrição | Dependências |
| --- | --- | --- |
| **Router multi-provedor** | Implementar camada que roteia prompts entre Gemini (modelos gemini-1.5) e OpenAI (GPT-4.1/4o) com base em tipo de tarefa, custo e SLA. | Ajustar `ai_module/ai_service.py` e `chat_service.py` para usar um `LLMOrchestrator` central, métricas em `monitoring_system.py`. |
| **Enriquecimento contextual** | Usar Gemini para sumarizar dados multivariados (vendas, estoque, clima) e gerar contexto estruturado antes da chamada ao modelo da OpenAI responsável por decisões. | Conectar `get_business_context()` a novos pipelines de features com `pandas`/`statsmodels`. |
| **Resposta multimodal** | Habilitar Gemini para gerar descrições visuais e rascunhos de dashboards que o frontend pode renderizar (por exemplo, JSON de cards e gráficos). | Extender API `/api/ai/generate-insight` para aceitar `response_format`. |

### 8.2 Pipeline analítico + MLOps
- **Pipelines versionados**: usar `mlflow` ou `dvc` para rastrear datasets e experimentos (MAE, MAPE, R²), com deploy automatizado via GitHub Actions.
- **Avaliação contínua**: combinar regressão linear (statsmodels) e Prophet, registrando métricas por produto no Redis + banco histórico.
- **Feature Store light**: expor serviço que guarda regressores exógenos (clima, campanhas) e permite Gemini/GPT gerar hipóteses.

### 8.3 Segurança e governança de LLMs
- **Vault de prompts**: criptografar chaves e prompts sensíveis, armazenando no backend (`/api/vault/llm`).
- **Auditoria LGPD**: logar prompts/respostas com hash (SHA-256) e registrar eventos críticos no smart contract `LGPDAuditRegistry`.
- **Políticas de consentimento**: permitir que titulares optem por uso dos dados em modelos generativos (toggle no portal LGPD).

### 8.4 Entregas priorizadas
| Horizonte | Entrega | Responsáveis |
| --- | --- | --- |
| 0-1 mês | Atualizar SDK OpenAI (`openai>=1.0`) com wrapper compatível; habilitar fallback Gemini→OpenAI. | Equipe IA + DevSecOps |
| 1-2 meses | Implementar orquestrador e dashboards de comparação (tempo de resposta, custo por chamada). | Equipe IA |
| 2-3 meses | Liberar insights multimodais consumidos pelo frontend e registrar auditoria na blockchain. | Equipe IA + Front |

---

## 9. Melhorias no FrontGoDgital

| Área | Dor identificada | Ação proposta | Impacto |
| --- | --- | --- | --- |
| Consumo de APIs | Páginas como `CardapioDigital` usam `fetch` com `http://localhost:8080`, gerando risco de mixed content em HTTPS. | Centralizar chamadas no `api.js` e usar `process.env.REACT_APP_API_URL` com fallback seguro. | Evita falhas em produção HTTPS e simplifica observabilidade. |
| Observabilidade UX | Falta telemetria para mapear abandono em fluxos LGPD/consentimento. | Integrar `web-vitals` + `OpenTelemetry` e expor eventos para Gemini sugerir otimizações. | Permite decisões data-driven sobre UI. |
| Modularização | Componentes longos (`PortalDireitosLGPD`, `DashboardAuditoria`) dificultam testes. | Extrair hooks (`useLGPDRequests`, `useDashboardMetrics`) e componentes atômicos com Storybook. | Aumenta reuso, cobertura de testes e facilita experimentos de IA. |
| IA no front | Chat atual consome apenas texto. | Adicionar widget alimentado por Gemini para resumos rápidos e ações sugeridas (cards). | Melhora adoção de IA pelos usuários finais. |

---

## 10. Melhorias no Backend (Spring Boot)

| Área | Gap | Ação proposta | Impacto |
| --- | --- | --- | --- |
| Integração LLM | `chat_service` e backend ainda não compartilham camadas de autorização/contexto. | Criar microserviço `llm-gateway` com autenticação mútua (mTLS) e fila de prompts (Kafka/RabbitMQ). | Reduz acoplamento e facilita auditoria LGPD. |
| Observabilidade | Falta tracing distribuído em `RestTemplate` e `WebClient`. | Instrumentar com OpenTelemetry + Grafana Tempo/Jaeger. | Diagnóstico rápido de gargalos IA↔backend. |
| Segurança | MFA ainda não implementado; tokens refresh sem rotação. | Adicionar suporte WebAuthn/Authenticator Apps e tabelas de rotação de refresh token. | Hardening LGPD e redução de riscos. |
| Dados públicos | Endpoints `/public/cardapio` expõem dados sem cache nem ETags. | Adicionar `@Cacheable` + `Cache-Control`/ETag, e gateway CDN-ready. | Melhor desempenho e economia de custos. |

---

## 11. Iniciativas de Plataforma
- **Infra-as-Code**: Provisionar infraestrutura (Redis, MySQL, blockchain permissionada) via Terraform + Ansible.
- **CI/CD unificado**: Pipeline que roda `pytest`, `mvn verify`, `npm test`, scans SAST/DAST e publica métricas.
- **Gestão de segredos**: Centralizar em HashiCorp Vault/AWS Secrets Manager com rotação automática para chaves OpenAI/Gemini.
- **Programa de conformidade**: Preparar evidências ISO 27001/SOC 2 com política de auditoria blockchain.

---

## 12. Diagnóstico funcional e possíveis bugs

| Módulo | Status de verificação | Achados | Ações recomendadas |
| --- | --- | --- | --- |
| `ai_module` | Revisão manual do serviço Flask e endpoints críticos (`/predict`, `/retrain`). | Código de retreinamento tinha bloco inacessível (indentação), impedindo `POST /api/ai/retrain`; ajustado no commit atual. Compatibilidade do `openai.ChatCompletion` com SDK >=1.0 continua pendente. | Criar teste de integração cobrindo retreinamento, atualizar SDK para nova interface (`OpenAI` client) e validar fallback Gemini. |
| `padariaApi` | Revisão de segurança e controllers. | Falta telemetria e auditoria detalhada de chamadas para IA; endpoints públicos sem caching. | Cobrir com testes `mvn test`, habilitar logs estruturados e aplicar cache/ETag nos endpoints públicos. |
| `FrontGoDgital` | Inspeção dos serviços e páginas principais. | Mixed content: `CardapioDigital` chama `http://localhost:8080` via `fetch`, quebrando quando servido em HTTPS; interceptors não tratam expiração simultânea de access/refresh token. | Migrar para `api.js`, usar HTTPS/variáveis ambiente e adicionar retry inteligente no interceptor. |
| Plataforma | Scripts `start_system.bat`/`system_status.bat` revisados. | Não há automação Linux/macOS; monitoramento distribuído depende de execução manual. | Adicionar scripts cross-platform (Makefile, docker-compose) e health-checks automatizados no CI. |

Checklist sugerido para homologação dos módulos:
1. `pytest -q` em `ai_module` após atualizar modelos.
2. `mvn clean verify` em `padariaApi` com banco em memória.
3. `npm run lint && npm test` no frontend usando `.env` com URL HTTPS.
4. Execução integrada via `docker-compose` validando chamadas LLM (Gemini/OpenAI) com chaves de sandbox.

---

## 13. Backlog paralelizável

| Tarefa | Time responsável | Dependências | Entrega |
| --- | --- | --- | --- |
| Atualizar SDKs LLM e implementar orquestrador | IA + DevSecOps | Disponibilidade de chaves Gemini/OpenAI de sandbox | Sprint atual |
| Refatorar consumo de APIs no frontend (`CardapioDigital`, widgets LGPD) | Front-end | Definição de `REACT_APP_API_URL` e contratos REST estáveis | Sprint atual |
| Instrumentar observabilidade (OpenTelemetry) no backend | Backend | Stack de observabilidade provisionada (Grafana/Tempo) | +1 sprint |
| Planejar PoC blockchain (deploy smart contract) | Plataforma | Ambiente Quorum/Besu provisionado | +1 sprint |
| Implementar pipeline estatístico (correlação/regressão) | Data/Analytics | Dados históricos limpos e definidos | +1 sprint |

---

> Atualizado em: novembro/2025 — Responsável: Equipe goDigital Code
