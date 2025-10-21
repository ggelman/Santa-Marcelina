# Sistema de Alertas de Segurança em Tempo Real

## Visão Geral

O **Sistema de Alertas de Segurança em Tempo Real** foi implementado para fornecer visibilidade imediata sobre eventos de segurança, rate limiting e proteção DDoS no GoDigital Padaria. Este sistema complementa a infraestrutura de segurança backend com uma interface frontend robusta e alertas em tempo real.

> Público-alvo: Administradores, Gerentes de TI e desenvolvedores com acesso ao painel.

## 🔧 Componentes Implementados

### 1. SecurityDashboard
**Localização:** `src/components/security/SecurityDashboard.js`

- **Dashboard principal** com métricas de segurança em tempo real
- **Auto-refresh** a cada 30 segundos
- **Métricas principais:**
  - Status do Rate Limiting
  - IPs monitorados e bloqueados
  - Total de requisições registradas
  - Alertas recentes

```javascript
// Uso básico
import SecurityDashboard from '../components/security/SecurityDashboard';

<SecurityDashboard />
```

### 2. SecurityAlertsProvider
**Localização:** `src/components/security/SecurityAlertsProvider.js`

- **Context Provider** para gerenciar alertas globalmente
- **Toast notifications** para alertas críticos
- **Auto-remoção** de toasts após 10 segundos
- **Painel de alertas** com filtros e controles

```javascript
// Uso em toda a aplicação
import { SecurityAlertsProvider, useSecurityAlerts } from '../components/security/SecurityAlertsProvider';

// No App.js
<SecurityAlertsProvider>
  <App />
</SecurityAlertsProvider>

// Em componentes
const { addAlert, alerts } = useSecurityAlerts();
```

### 3. SecurityMetrics
**Localização:** `src/components/security/SecurityMetrics.js`

- **Gráficos interativos** usando Recharts
- **Múltiplos tipos de visualização:**
  - Linha temporal de requisições
  - Gráficos de barras para rate limiting
  - Gráficos de pizza para distribuição de ameaças
  - Tabelas de top IPs
- **Filtros de tempo:** 1h, 24h, 7d

### 4. SecurityMonitoringPage
**Localização:** `src/pages/SecurityMonitoringPage.js`

- **Página dedicada** com navegação por abas
- **Tabs principais:**
  - Dashboard: Visão geral em tempo real
  - Métricas: Gráficos e análises detalhadas
  - Alertas: Lista completa de alertas
  - Configurações: Ajustes do sistema

## 🚨 Tipos de Alertas

### Críticos (Vermelho)
- IPs bloqueados por atividade suspeita
- Falhas de segurança detectadas
- Tentativas de ataque DDoS

### Atenção (Amarelo)
- Rate limits excedidos
- Alto volume de tráfego
- Padrões suspeitos detectados

### Informativos (Azul)
- Status do sistema
- Atualizações de configuração
- Métricas normais

### Sucesso (Verde)
- Sistema funcionando normalmente
- Bloqueios preventivos efetivos
- Configurações aplicadas com sucesso

## 🔄 Monitoramento Automático

### Hook useSecurityMonitoring
**Localização:** `src/hooks/useSecurityMonitoring.js`

```javascript
import { useSecurityMonitoring } from '../hooks/useSecurityMonitoring';

const { startMonitoring } = useSecurityMonitoring();

useEffect(() => {
  const stopMonitoring = startMonitoring();
  return stopMonitoring;
}, []);
```

### Funcionalidades de Monitoramento

1. **Verificação de Ameaças**: A cada 60 segundos
2. **Métricas em Tempo Real**: A cada 30 segundos
3. **Notificações do Browser**: Para alertas críticos
4. **Logging Automático**: Todos os eventos são registrados

## 📊 APIs Utilizadas

### Backend Spring Boot
- `/api/ai/security/stats` - Estatísticas gerais
- `/api/ai/security/health` - Status do sistema
- `/api/ai/security/settings` - Configurações
 - `/api/ai/security/export-logs` - Exportação de logs em JSON

### Backend Python (AI Module)
- `/ai/security/stats` - Estatísticas do AI Module
- `/ai/rate-limits` - Status do rate limiting
- `/ai/security/check-threats` - Verificação de ameaças
- `/ai/security/metrics` - Métricas detalhadas

> Observação: os endpoints acima podem ser adaptados na camada de API. Garanta que o frontend e o backend estejam alinhados quanto ao formato de resposta.

#### Contratos de resposta esperados (exemplos)

- `/api/ai/security/health`
  ```json
  { "status": "healthy" } // valores possíveis: healthy | warning | critical | unknown
  ```

- `/api/ai/security/stats`
  ```json
  {
    "rate_limits": { "login": {"limit": 5, "current": 2}, "api": {"limit":100,"current":40} },
    "blocked_ips": ["203.0.113.15"],
    "top_ips_by_volume": [{"ip":"198.51.100.8","count":123}],
    "alerts": [{"type":"critical","message":"Ataque detectado","timestamp":"2025-10-01T12:00:00Z"}]
  }
  ```

- `/ai/security/metrics?range=24h`
  ```json
  {
    "traffic": [{"ts":"2025-10-01T12:00:00Z","count":120}],
    "rateLimiter": [{"bucket":"api","used":40,"limit":100}],
    "threats": [{"name":"Bot","value":12}],
    "topIps": [{"ip":"198.51.100.8","count":123}]
  }
  ```

## 🎨 Interface do Usuário

### Indicadores Visuais
- **Badges numerados** no menu lateral para alertas não lidos
- **Cores consistentes** para diferentes tipos de alertas
- **Ícones intuitivos** para fácil identificação
- **Animações suaves** para transições e toasts

### Responsividade
- **Design responsivo** para desktop e mobile
- **Grid layouts** que se adaptam ao tamanho da tela
- **Navegação otimizada** para diferentes dispositivos

## 🔧 Configurações Disponíveis

### Rate Limiting
- **Login**: Limite por minuto (padrão: 5)
- **API**: Limite por minuto (padrão: 100)
- **AI**: Limite por minuto (padrão: 10)
- **Operações Pesadas**: Limite por hora (padrão: 20)

### Monitoramento
- **Alertas**: Habilitar/desabilitar
- **Bloqueio Automático**: Ativar bloqueio de IPs suspeitos
- **Limite para Alerta**: Número de requisições para gerar alerta
- **Duração do Bloqueio**: Tempo em segundos

### Notificações
- **Email**: Notificações por email
- **Browser**: Notificações do navegador
- **Apenas Críticos**: Filtrar apenas alertas críticos

## 🚀 Como Utilizar

### 1. Acesso Básico
1. Faça login como **Administrador** ou **Gerente**
2. Clique em **"🔒 Security Monitor"** no menu lateral
3. O badge vermelho indica alertas não lidos

### 2. Visualização de Alertas
- **Dashboard**: Visão geral em tempo real
- **Toasts**: Notificações automáticas para eventos críticos
- **Painel de Alertas**: Lista completa com filtros

#### Marcando alertas como lidos
- Use a ação no painel de alertas para marcar itens como lidos e limpar badges.

### 3. Análise de Métricas
- Acesse a aba **"Métricas"**
- Selecione o período de análise (1h, 24h, 7d)
- Analise gráficos de tráfego, rate limiting e ameaças

### 4. Configuração do Sistema
- Acesse a aba **"Configurações"**
- Ajuste limites de rate limiting
- Configure notificações e monitoramento

### 5. Exportação de Logs
- Na barra superior da página de monitoramento, use **Exportar Logs** para baixar um JSON com eventos das últimas 24h.
- Endpoint utilizado: `/api/ai/security/export-logs` (POST com `{ "timeRange": "24h", "includeMetrics": true }`).

### 6. Notificações do Navegador
- Ao acessar o painel, o sistema pode pedir permissão de notificação.
- Para alertas críticos, as notificações aparecem mesmo fora da aba (se permitido).

## 📈 Benefícios Implementados

### Visibilidade em Tempo Real ✅
- **Dashboard interativo** com atualizações automáticas
- **Métricas visuais** com gráficos e indicadores
- **Alertas instantâneos** para eventos críticos

### Notificações Proativas ✅
- **Toast notifications** para alertas críticos
- **Badges numerados** no menu de navegação
- **Notificações do browser** (com permissão do usuário)

### Análise Histórica ✅
- **Gráficos temporais** de atividade
- **Análise de padrões** de ameaças
- **Relatórios de top IPs** por volume

### Controle Administrativo ✅
- **Configurações centralizadas** de segurança
- **Exportação de logs** para análise externa
- **Controles granulares** de rate limiting

## 🔒 Segurança e Privacidade

### Dados Protegidos
- **Apenas IPs ofuscados** são exibidos quando necessário
- **Logs estruturados** sem exposição de dados sensíveis
- **Acesso restrito** a usuários com permissões administrativas

### Conformidade
- **Logs auditáveis** para conformidade
- **Retenção configurável** de dados
- **Anonização automática** de dados antigos

## 🛠️ Manutenção e Suporte

### Monitoramento do Sistema
- **Health checks** automáticos do sistema
- **Alertas de falha** em componentes críticos
- **Métricas de performance** do próprio sistema de alertas

### Troubleshooting
1. **Alertas não aparecem**: Verificar permissões de usuário
2. **Gráficos não carregam**: Verificar conectividade com backend
3. **Notificações não funcionam**: Verificar permissões do browser


### Logs de Desenvolvimento
```javascript
// Para debug, ativar logs detalhados
localStorage.setItem('security_debug', 'true');
```

## 📋 Próximos Passos

### Melhorias Sugeridas
- [ ] **WebSocket** para atualizações em tempo real
- [ ] **Alertas por email** configuráveis
- [ ] **Dashboard executivo** com métricas de alto nível
- [ ] **Integração com SIEM** externos
- [ ] **Análise de comportamento** com Machine Learning

### Integrações Futuras
- [ ] **Slack/Teams** para notificações de equipe
- [ ] **API de geolocalização** para análise de IPs
- [ ] **Integração com WAF** (Web Application Firewall)
- [ ] **Alertas customizáveis** por usuário

---

## 📞 Suporte

Para dúvidas ou problemas com o sistema de alertas de segurança:

1. **Documentação técnica**: Consulte os comentários no código
2. **Logs do sistema**: Acesse via Console do navegador (F12)
3. **Exportação de dados**: Use a função de exportar logs na interface

**Status atual: ✅ IMPLEMENTADO E FUNCIONAL**

O sistema está pronto para uso em produção com todas as funcionalidades de segurança ativas e monitoramento em tempo real operacional.

---

## 🧪 Testes Rápidos (Dev)

Use estes passos para validar rapidamente em desenvolvimento:

1. Backend Java (Spring Boot)
  - Certifique-se de que a API está rodando (ex.: `http://localhost:8080`).
2. Frontend Next.js/React
  - Inicie a aplicação web e acesse a rota `/security`.
3. Simular tráfego/limites
  - Gere múltiplas requisições para endpoints protegidos e observe os gráficos e alertas.
4. Verificar health
  - Acesse o painel e confirme o badge de status (Healthy/Warning/Critical) no cabeçalho.

## 🔐 Permissões e Acesso

- Recomendado: restringir o acesso ao menu e à rota `/security` a perfis de Administrador/Segurança.
- Auditoria: registre quem acessa o painel e quais ações executa (exportações, mudanças de configuração).