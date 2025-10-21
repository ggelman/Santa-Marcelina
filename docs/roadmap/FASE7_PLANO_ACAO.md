# 🚦 Plano de Ação — Fase 7 (0-3 meses)
> Hardening de segurança, observabilidade integrada e estatística aplicada.

## 🎯 Objetivos desta fase
- Entregar autenticação multifator (MFA/WebAuthn) para perfis administrativos em todo o ecossistema.
- Integrar o backend e o módulo de IA a um SIEM corporativo com telemetria OpenTelemetry.
- Publicar o pipeline estatístico de correlação/regressão com dashboards operacionais.
- Automatizar backups, rotação de segredos e verificações de integridade de auditoria LGPD.

## 🗓️ Organização em sprints (12 semanas)
| Semana | Foco principal | Entregas chave | Responsáveis |
| --- | --- | --- | --- |
| 1-2 | Kick-off e fundações | • Revisão de arquitetura de segurança<br>• Definição do provedor de MFA e SIEM<br>• Roadmap técnico aprovado por squads | PMO + Tech Leads |
| 3-4 | MFA administrativo | • Proof-of-concept WebAuthn + TOTP<br>• UI/UX atualizada (frontend)<br>• Serviços Spring Boot com desafios mTLS | Backend + Frontend |
| 5-6 | Observabilidade distribuída | • Instrumentação OpenTelemetry no backend e IA<br>• Pipelines de ingestão no SIEM<br>• Alertas críticos definidos | Backend + IA + SecOps |
| 7-8 | Pipeline estatístico | • ETL de dados de vendas/consentimentos<br>• Modelos de correlação e regressão versionados<br>• Dashboards React consumindo APIs analytics | IA/Data + Frontend |
| 9-10 | Automação de backups e segredos | • Scripts Terraform/Ansible para rotinas agendadas<br>• Vault/Secrets Manager integrado ao CI/CD<br>• Testes de restauração documentados | DevSecOps |
| 11-12 | Homologação e auditoria | • Execução da suíte de testes e cargas<br>• Geração do pacote de evidências executivas<br>• Retrospectiva com lições aprendidas | Todos os squads |

## 🧩 Trilha de trabalho por domínio
### Backend (Spring Boot)
- [ ] Criar microserviço `llm-gateway` com autenticação mTLS e fila de prompts (RabbitMQ/Kafka).
- [ ] Implementar fluxo WebAuthn + fallback TOTP para contas administrativas.
- [ ] Habilitar refresh token rotation com invalidação em cascata.
- [ ] Instrumentar tracing distribuído (OpenTelemetry) e exportar para o SIEM.
- [ ] Adicionar cache/ETag nas rotas públicas (`/portal/*`, `/status/*`).

### Frontend (React)
- [ ] Atualizar `src/services/api.js` com interceptors para MFA e rotação segura de tokens.
- [ ] Modularizar telas administrativas extensas utilizando hooks compartilhados.
- [ ] Exibir widget Gemini com insights rápidos e indicadores estatísticos.
- [ ] Instrumentar Web Vitals e exportar métricas para o coletor OpenTelemetry.

### Módulo de IA & Analytics
- [ ] Atualizar SDKs OpenAI/Gemini e validar fallback automático.
- [ ] Construir orquestrador multi-provedor com métricas comparativas (latência/custo/qualidade).
- [ ] Versionar pipelines no MLflow/DVC com registro de experimentos.
- [ ] Disponibilizar API de correlação/regressão com cache Redis e telemetria.

### Plataforma, Infra & DevSecOps
- [ ] Padronizar IaC (Terraform/Ansible) para provisionar serviços de SIEM, Vault e filas.
- [ ] Automatizar backups incrementais + full com testes de restauração trimestrais.
- [ ] Integrar pipelines de CI/CD com scans SAST/DAST e gatilhos de conformidade.
- [ ] Orquestrar execução `docker compose` para ambientes locais com chaves LLM de sandbox.
- [ ] Preparar documentação ISO/SOC alinhada com auditoria blockchain-ready.

## 🔗 Dependências e integrações críticas
- MFA depende do alinhamento com o IdP corporativo (LDAP/AD ou Auth0/Azure AD).
- SIEM requer conectores OpenTelemetry Collector + agentes nos hosts do backend e IA.
- Pipelines estatísticos necessitam acesso a dados de vendas, consentimentos e logs de auditoria (governança LGPD obrigatória).
- Backups automatizados exigem storage imutável com versionamento e políticas de retenção aprovadas pela compliance.

## ✅ Critérios de conclusão
1. Todos os perfis administrativos exigem MFA na autenticação e na elevação de privilégios.
2. Dashboard SIEM exibe métricas do backend, frontend (Web Vitals) e IA em tempo real.
3. Relatórios de correlação/regressão disponíveis no frontend com trilha de auditoria blockchain.
4. Backups são executados automaticamente, testados e versionados com hash registrado na blockchain permissionada.
5. Checklists de validação executados (`pytest -q`, `mvn clean verify`, `npm run lint && npm test`, `docker compose up -d`).

## 📊 Indicadores de acompanhamento
- Tempo médio para resposta a incidentes (meta: < 15 min de detecção → alerta SIEM).
- Taxa de sucesso MFA por usuário administrativo (> 98%).
- Latência média do orquestrador LLM (< 2s p/ principais rotas).
- Precisão dos modelos estatísticos (MAPE < 10% para previsões de demanda).
- Percentual de backups verificados com sucesso (100% por trimestre).

## ⚠️ Riscos e mitigação
| Risco | Probabilidade | Impacto | Mitigação |
| --- | --- | --- | --- |
| Integração MFA atrasada por dependência externa | Média | Alta | Antecipar testes com ambiente sandbox do IdP e definir fallback TOTP offline. |
| Sobrecarga no SIEM devido ao volume de logs | Média | Média | Definir sampling e agregação no OpenTelemetry Collector, revisando limites contratados. |
| Dados estatísticos inconsistentes | Baixa | Alta | Governança de dados com catálogo, validação automatizada e data stewardship. |
| Falhas em backups automatizados | Baixa | Alta | Monitoramento diário dos jobs e exercícios de restauração supervisionados. |

## 📁 Pacote de evidências
- Diagramas atualizados da arquitetura e fluxos MFA/WebAuthn.
- Relatórios de testes (unitários, integração e carga) anexados ao Confluence/Jira.
- Logs de auditoria com hash blockchain e checklist de conformidade LGPD.
- Guia rápido para equipes executivas com resumo dos indicadores e ROI esperado.

> Última atualização: dezembro/2025 — manter revisão quinzenal durante a execução da fase.
