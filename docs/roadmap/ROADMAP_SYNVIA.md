# Synvia Platform – Roadmap Consolidado
_Atualizado em: outubro/2025_

## Visão Geral
Após a migração do monólito goDigital para a identidade Synvia, o ambiente local foi padronizado em **HTTP por padrão** (AI 5001, Core API 8080, Front 3000) com suportes opcionais a TLS documentados. O objetivo agora é evoluir a plataforma para uma experiência modular multissetor, mantendo observabilidade e segurança como pilares.

### Status por Domínio
| Módulo | Status atual | Destaques recentes | Pontos de atenção |
| --- | --- | --- | --- |
| **Synvia Front (React)** | 85% | Branding Synvia aplicado, tema centralizado, endpoints HTTP configuráveis via `.env`. | Persistem páginas longas sem hooks dedicados e falta cobertura de testes (Jest/Lint). |
| **Synvia Core API (Spring Boot)** | 85% | Build `mvn clean verify` estabilizado, cache ativado (Caffeine), execução default em HTTP 8080. | A integração LLM ainda é acoplada, faltam MFA/WebAuthn e observabilidade distribuída. |
| **Synvia Intelligence (Flask/IA)** | 80% | Rotas principais em 5001, cache/monitoring ativos, novos templates de `.env`. | SDKs OpenAI/Gemini desatualizados, falta orquestrador multi-provedor e testes automatizados. |
| **Infra & DevSecOps** | 70% | Scripts de start/stop/status revisados para HTTP; credenciais padronizadas. | Ausência de automações cross-platform, CI/CD integrado e gestão centralizada de segredos. |

## Destaques Recentes
- Reconfiguração total para **execução em HTTP**: `start_system.bat`, `stop_system.bat`, `system_status.bat` e `test_sistema_seguranca.bat` alinham portas 3000/8080/5001.
- Eliminação de resíduos legados (`padariaApi/`) e criação de templates `.env.example` para Front e IA.
- Documentação revisada (Guias rápido e completo, README principal) refletindo o novo fluxo Synvia.

## Prioridades Atuais (0-4 semanas)
1. **Front**  
   - Extrair hooks/componentes das páginas LGPD (`PortalDireitos`, `DashboardAuditoria`, `CadastroClientePublico`).  
   - Implementar suíte de testes (`npm run lint && npm test`) e pipeline GitHub Actions.  
   - Adicionar fallback de erro e toasts unificados para chamadas API.

2. **Core API**  
   - Configurar MFA/WebAuthn + rotação de refresh tokens.  
   - Instrumentar OpenTelemetry (traços + métricas) e publicar dashboards Grafana.  
   - Criar camada `llm-gateway` (mTLS + fila de prompts) desacoplando IA externa.

3. **Intelligence**  
   - Atualizar SDKs (`openai`, `google-generativeai`) e adequar chamadas.  
   - Implementar orchestrator multi-provider com estratégia de fallback/custo.  
   - Adicionar testes `pytest` para `/predict`, `/retrain`, `/health` e pipeline de retreinamento.

4. **Plataforma/DevSecOps**  
   - Criar scripts multiplataforma (`Makefile`/`npm scripts`) e compose local.  
   - Configurar CI/CD unificado (pytest, mvn verify, npm test, lint, SAST).  
   - Definir vault de segredos (HashiCorp Vault ou Secrets Manager) e processo de rotação.

## Backlog Estruturado
### Sincronismo (1-2 sprints)
- **Front**: widget Synvia Insights (chat Gemini), reporter web-vitals, Storybook de componentes.
- **Core API**: caching ETag em endpoints públicos, perfis multi-tenant, testes de integração `RestAssured`.
- **IA**: monitoramento de drift automático, logging estruturado enviado para Core API.
- **Infra**: IaC (Terraform + Ansible) para provisionar MySQL, Redis, colletores OTel.

### Médio Prazo (3-6 sprints)
- Multi-tenant real (escopos por cliente) + RBAC avançado.
- PoC de blockchain permissionada para auditoria LGPD (Hyperledger Besu).
- Experiência omnichannel (exposição de APIs GraphQL/gRPC).

## Próximas Tarefas Curadas
| Módulo | Tarefa | Responsável sugerido | Saída esperada |
| --- | --- | --- | --- |
| Synvia Front | Refatorar `CardapioDigital` e `PortalDireitosLGPD` em hooks + testes | Front-end | Componentes desacoplados, cobertura Jest >70% |
| Synvia Core | Implementar MFA + refresh rotation + endpoints de auditoria | Backend | Segurança reforçada, novos fluxos documentados |
| Synvia Intelligence | Atualizar SDKs LLM e criar orquestrador com retries/logs | IA/Data | Clientes `gemini`/`openai` modernos, fallback inteligente |
| DevSecOps | Pipeline CI/CD integrado (pytest/mvn/npm + lint + relatório) | DevOps | Execução automática em PRs com status visível |

## Links Úteis
- **Ambiente HTTP**: consulte `README.md` e `docs/guides/INICIO_RAPIDO.md`.
- **Templates `.env`**: `FrontGoDgital/.env.example` e `ai_module/.env.example`.
- **Script de status**: `system_status.bat` (verifica 3000/8080/5001).

> Para evoluções de longo prazo (ex.: blockchain, SaaS multi-tenant), registre novas iniciativas nesta página e referencie suas epics no sistema de gestão que a equipe escolher.
