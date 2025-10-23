# 🛡️ Rate Limiting e DDoS Protection - Synvia Platform

**Data:** 01/10/2025  
**Versão:** 1.0.0  
**Status:** Implementado  

## 📋 Visão Geral

Sistema abrangente de Rate Limiting e DDoS Protection implementado em ambas as camadas do sistema:
- **Backend Spring Boot**: Bucket4j com filtros personalizados
- **AI Module Python**: Flask-Limiter com monitoramento de segurança

## 🔧 Configurações Implementadas

### 🏢 **Backend (Spring Boot)**

#### **Políticas de Rate Limiting**
```java
// Login: 5 requests por minuto por IP
LOGIN: 5 requests/minute

// APIs Gerais: 100 requests por minuto por IP  
API: 100 requests/minute

// AI Proxy: 10 requests por minuto por IP
AI: 10 requests/minute

// Operações Pesadas: 20 requests por hora por IP
HEAVY_OPERATION: 20 requests/hour
```

#### **Endpoints Protegidos**
- ✅ `/api/auth/login` - 5/min (proteção força bruta)
- ✅ `/api/ai/**` - 10/min (proteção proxy IA)
- ✅ `/api/backup/**` - 20/hour (operações pesadas)
- ✅ `/api/relatorios/**` - 20/hour (operações pesadas)
- ✅ Demais APIs - 100/min (uso geral)

#### **Headers de Resposta**
```http
X-Rate-Limit-Remaining: 95
X-Rate-Limit-Bucket-Type: API
X-Rate-Limit-Retry-After-Seconds: 60
```

### 🤖 **AI Module (Python Flask)**

#### **Políticas Específicas**
```python
# Limites globais por IP
default_limits = ["200 per day", "50 per hour"]

# Endpoints específicos:
predict-all: 10 per minute      # Previsões bulk
predict: 15 per minute          # Previsões individuais  
retrain: 2 per hour             # Retreinamento (muito pesado)
generate-insight: 20 per hour   # Insights IA (API externa)
```

#### **Monitoramento de Segurança**
```python
# Thresholds de detecção
requests_per_minute: 100        # Volume suspeito
failed_requests_per_minute: 20  # Força bruta
unique_endpoints_per_minute: 50 # Scanning
```

## 🚨 Proteções Implementadas

### 🛡️ **Anti-DDoS Mechanisms**

1. **Volume-based Protection**
   - Limite por IP por endpoint
   - Buckets separados por tipo de operação
   - Reset automático com janelas deslizantes

2. **Pattern Detection**
   - Alto volume de requests (>100/min)
   - Alto número de falhas (>20/min) 
   - Scanning de endpoints (>50 únicos/min)
   - User-agents suspeitos

3. **Automatic Response**
   - HTTP 429 (Too Many Requests)
   - Headers informativos
   - Bloqueio temporário de IPs suspeitos
   - Logs detalhados de segurança

### 📊 **Monitoring & Alerting**

#### **Endpoints de Monitoramento**
```bash
# Status dos rate limits
GET /api/ai/rate-limits

# Estatísticas de segurança  
GET /api/security/stats

# Health check com limites
GET /api/ai/health
```

#### **Logs de Segurança**
```json
{
  "timestamp": "2025-10-01T15:30:00Z",
  "ip": "192.168.1.100", 
  "type": "HIGH_VOLUME",
  "details": "150 requests in 1 minute",
  "action": "MONITOR"
}
```

## ⚙️ Configuração e Deployment

### 🔧 **Dependências Adicionadas**

#### **Backend (pom.xml)**
```xml
<dependency>
    <groupId>com.github.vladimir-bukhtoyarov</groupId>
    <artifactId>bucket4j-core</artifactId>
    <version>7.6.0</version>
</dependency>
<dependency>
    <groupId>com.github.vladimir-bukhtoyarov</groupId>
    <artifactId>bucket4j-caffeine</artifactId>
    <version>7.6.0</version>
</dependency>
```

#### **AI Module (requirements.txt)**
```text
flask-limiter
slowapi
```

### 🚀 **Inicialização**

Os rate limits são ativados automaticamente quando os serviços iniciam:
- **Spring Boot**: Filtro aplicado antes da autenticação
- **Flask**: Limiter configurado no app initialization

## 📈 Métricas e KPIs

### 🎯 **Métricas de Segurança**
- Requests bloqueados por rate limiting
- IPs únicos monitorados  
- Padrões suspeitos detectados
- Tempo de resposta com limitação

### 📊 **Dashboards**
- Volume de requests por endpoint
- Top IPs por volume de requisições
- Distribuição de status codes
- Alertas de segurança em tempo real

## 🔍 Testes e Validação

### ✅ **Cenários de Teste**

1. **Login Brute Force**
   ```bash
   # Deve bloquear após 5 tentativas/minuto
   for i in {1..10}; do 
     curl -X POST /api/auth/login
   done
   ```

2. **API Flooding**
   ```bash
   # Deve bloquear após 100 requests/minuto
   ab -n 150 -c 10 http://localhost:8080/api/produtos
   ```

3. **AI Endpoint Abuse**
   ```bash
   # Deve bloquear após 10 requests/minuto
   for i in {1..15}; do
     curl http://localhost:5001/api/ai/predict-all
   done
   ```

## 🚨 Alertas e Resposta a Incidentes

### 📋 **Tipos de Alertas**
- `HIGH_VOLUME`: Muito volume de requests
- `HIGH_FAILURE_RATE`: Muitas falhas 4xx/5xx
- `ENDPOINT_SCANNING`: Tentativa de descoberta
- `IP_BLOCKED`: Bloqueio automático ativado

### 🔧 **Ações Automáticas**
- Rate limiting progressivo
- Bloqueio temporário (1 hora)
- Logs estruturados para SIEM
- Headers informativos para debugging

## 🎯 Próximos Passos

### 🔄 **Melhorias Recomendadas**
1. **Redis Backend**: Compartilhar rate limits entre instâncias
2. **Geolocation**: Bloqueio por país/região
3. **Machine Learning**: Detecção de padrões avançada  
4. **WAF Integration**: Integração com Web Application Firewall
5. **Adaptive Limits**: Ajuste dinâmico baseado em carga

### 📊 **Monitoring Avançado**
- Integração com Prometheus/Grafana
- Alertas via PagerDuty/Slack
- Dashboard executivo de segurança
- Relatórios de compliance

## ✅ Status de Implementação

- ✅ **Rate Limiting Backend**: Implementado e testado
- ✅ **Rate Limiting AI Module**: Implementado e testado  
- ✅ **Security Monitoring**: Sistema de detecção ativo
- ✅ **Alerting System**: Logs estruturados funcionando
- ✅ **Response Headers**: Informações para debugging
- ✅ **Health Checks**: Monitoramento de status

**Sistema de Rate Limiting e DDoS Protection totalmente funcional e pronto para produção!** 🚀
