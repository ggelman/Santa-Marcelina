# 🗺️ Roadmap Estratégico de Transformação Digital
> goDigital Code — Padaria Santa Marcelina

## 0. Contexto
Com a maturidade em LGPD e Governança de TI atingida, o foco agora é posicionar o goDigital Code como plataforma de mercado. O roadmap abaixo consolida o estado atual do projeto e direciona as evoluções necessárias para incorporar Blockchain, Smart Contracts, estatística aplicada e práticas avançadas de segurança.

---

## 1. Status Consolidado da Implementação

| Módulo | Situação | Destaques atuais | Próximos ajustes |
| --- | --- | --- | --- |
| FrontGoDgital (React) | 85% — operacional | Dashboard de auditoria, Portal de Direitos, módulos administrativos. | Modularizar componentes reutilizáveis e ampliar testes automatizados. |
| padariaApi (Spring Boot) | 85% — operacional | APIs LGPD, autenticação JWT, integração IA. | Implementar auditoria blockchain-ready e camadas anti-fraude. |
| ai_module (Flask/ML) | 80% — operacional | Previsões de demanda, monitoramento estruturado, cache Redis. | Treinar modelos com pipelines de MLOps e métricas comparativas (MAE/MAPE). |
| Infraestrutura & DevSecOps | 70% — parcial | Certificados SSL, scripts de orquestração, logging básico. | Automatizar CI/CD, backup versionado e centralizar observabilidade. |

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

> Atualizado em: outubro/2025 — Responsável: Equipe goDigital Code
