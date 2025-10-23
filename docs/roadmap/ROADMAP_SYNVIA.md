# Synvia Platform â€“ Roadmap Consolidado
_Atualizado em: outubro/2025_

## VisÃ£o Geral
ApÃ³s a migraÃ§Ã£o do monÃ³lito goDigital para a identidade Synvia, o ambiente local foi padronizado em **HTTP por padrÃ£o** (AI 5001, Core API 8080, Front 3000) com suportes opcionais a TLS documentados. O objetivo agora Ã© evoluir a plataforma para uma experiÃªncia modular multissetor, mantendo observabilidade e seguranÃ§a como pilares.

### Status por DomÃ­nio
| MÃ³dulo | Status atual | Destaques recentes | Pontos de atenÃ§Ã£o |
| --- | --- | --- | --- |
| **Synvia Front (React)** | 85% | Branding Synvia aplicado, tema centralizado, endpoints HTTP configurÃ¡veis via `.env`. | Persistem pÃ¡ginas longas sem hooks dedicados e falta cobertura de testes (Jest/Lint). |
| **Synvia Core API (Spring Boot)** | 85% | Build `mvn clean verify` estabilizado, cache ativado (Caffeine), execuÃ§Ã£o default em HTTP 8080. | A integraÃ§Ã£o LLM ainda Ã© acoplada, faltam MFA/WebAuthn e observabilidade distribuÃ­da. |
| **Synvia Intelligence (Flask/IA)** | 80% | Rotas principais em 5001, cache/monitoring ativos, novos templates de `.env`. | SDKs OpenAI/Gemini desatualizados, falta orquestrador multi-provedor e testes automatizados. |
| **Infra & DevSecOps** | 70% | Scripts de start/stop/status revisados para HTTP; credenciais padronizadas. | AusÃªncia de automaÃ§Ãµes cross-platform, CI/CD integrado e gestÃ£o centralizada de segredos. |

## Destaques Recentes
- ReconfiguraÃ§Ã£o total para **execuÃ§Ã£o em HTTP**: `start_system.bat`, `stop_system.bat`, `system_status.bat` e `test_sistema_seguranca.bat` alinham portas 3000/8080/5001.
- DocumentaÃ§Ã£o revisada (Guias rÃ¡pido e completo, README principal) refletindo o novo fluxo Synvia.

## Prioridades Atuais (0-4 semanas)
1. **Front**  
   - Extrair hooks/componentes das pÃ¡ginas LGPD (`PortalDireitos`, `DashboardAuditoria`, `CadastroClientePublico`).  
   - Implementar suÃ­te de testes (`npm run lint && npm test`) e pipeline GitHub Actions.  
   - Adicionar fallback de erro e toasts unificados para chamadas API.

2. **Core API**  
   - Configurar MFA/WebAuthn + rotaÃ§Ã£o de refresh tokens.  
   - Instrumentar OpenTelemetry (traÃ§os + mÃ©tricas) e publicar dashboards Grafana.  
   - Criar camada `llm-gateway` (mTLS + fila de prompts) desacoplando IA externa.

3. **Intelligence**  
   - Atualizar SDKs (`openai`, `google-generativeai`) e adequar chamadas.  
   - Implementar orchestrator multi-provider com estratÃ©gia de fallback/custo.  
   - Adicionar testes `pytest` para `/predict`, `/retrain`, `/health` e pipeline de retreinamento.

4. **Plataforma/DevSecOps**  
   - Criar scripts multiplataforma (`Makefile`/`npm scripts`) e compose local.  
   - Configurar CI/CD unificado (pytest, mvn verify, npm test, lint, SAST).  
   - Definir vault de segredos (HashiCorp Vault ou Secrets Manager) e processo de rotaÃ§Ã£o.

## Backlog Estruturado
### Sincronismo (1-2 sprints)
- **Front**: widget Synvia Insights (chat Gemini), reporter web-vitals, Storybook de componentes.
- **Core API**: caching ETag em endpoints pÃºblicos, perfis multi-tenant, testes de integraÃ§Ã£o `RestAssured`.
- **IA**: monitoramento de drift automÃ¡tico, logging estruturado enviado para Core API.
- **Infra**: IaC (Terraform + Ansible) para provisionar MySQL, Redis, colletores OTel.

### MÃ©dio Prazo (3-6 sprints)
- Multi-tenant real (escopos por cliente) + RBAC avanÃ§ado.
- PoC de blockchain permissionada para auditoria LGPD (Hyperledger Besu).
- ExperiÃªncia omnichannel (exposiÃ§Ã£o de APIs GraphQL/gRPC).

## PrÃ³ximas Tarefas Curadas
| MÃ³dulo | Tarefa | ResponsÃ¡vel sugerido | SaÃ­da esperada |
| --- | --- | --- | --- |
| Synvia Front | Refatorar `CardapioDigital` e `PortalDireitosLGPD` em hooks + testes | Front-end | Componentes desacoplados, cobertura Jest >70% |
| Synvia Core | Implementar MFA + refresh rotation + endpoints de auditoria | Backend | SeguranÃ§a reforÃ§ada, novos fluxos documentados |
| Synvia Intelligence | Atualizar SDKs LLM e criar orquestrador com retries/logs | IA/Data | Clientes `gemini`/`openai` modernos, fallback inteligente |
| DevSecOps | Pipeline CI/CD integrado (pytest/mvn/npm + lint + relatÃ³rio) | DevOps | ExecuÃ§Ã£o automÃ¡tica em PRs com status visÃ­vel |


> Para evoluÃ§Ãµes de longo prazo (ex.: blockchain, SaaS multi-tenant), registre novas iniciativas nesta pÃ¡gina e referencie suas epics no sistema de gestÃ£o que a equipe escolher.

