# 🚀 Guia Completo de Execução

Procedimento detalhado para preparar e executar todos os módulos do goDigital Code com HTTPS opcional e validações pós-start.

---

## 1. Pré-requisitos

| Componente | Versão recomendada | Verificação |
| --- | --- | --- |
| Java | 17 ou superior | `java -version` |
| Maven | 3.8 ou superior | `mvn -version` |
| Node.js | 18 LTS | `node --version` |
| npm | 8 ou superior | `npm --version` |
| Python | 3.10 ou superior | `python --version` |

> Dica: em Windows, instale o [WSL](https://learn.microsoft.com/windows/wsl/install) para uma experiência mais próxima ao ambiente de produção.

---

## 2. Preparação do ambiente

### 2.1 Dependências do módulo de IA
```bash
cd ai_module
python -m venv .venv  # opcional
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

### 2.2 Dependências do frontend React
```bash
cd FrontGoDgital
npm install
```

### 2.3 Certificados e perfis HTTPS
- Certificados pré-gerados vivem em `ssl_certificates/` (`server.crt`, `server.key`, `keystore.p12`).
- Para rodar o backend em HTTPS utilize o perfil `https` (`mvn spring-boot:run -Dspring-boot.run.profiles=https`).
- O frontend roda em HTTP por padrão; configure proxies HTTPS somente se necessário.

---

## 3. Inicialização dos serviços

### 3.1 AI Service (Flask)
```bash
cd ai_module
python ai_service.py
```
- Porta padrão: `5443` (HTTPS com certificados incluídos). Para HTTP use `USE_HTTPS=false` e a porta passará a ser `5001`.
- Endpoints principais: `/predict`, `/health`, `/monitoring`.

### 3.2 Backend Spring Boot
```bash
cd synvia-core
mvn spring-boot:run
```
- Porta padrão: `8080` (HTTP) ou `8443` com o perfil HTTPS.
- A URL base da API é `/api`.

### 3.3 Frontend React
```bash
cd FrontGoDgital
npm start
```
- Porta padrão: `3000`.
- O proxy para o backend está configurado no `package.json` para `http://localhost:8080`.

> Em Windows, os scripts `start_system.bat` e `stop_system.bat` automatizam a orquestração.

---

## 4. Pós-start e validações

### 4.1 Health-checks essenciais
```bash
curl -k https://localhost:5443/health
curl http://localhost:8080/actuator/health
curl http://localhost:3000 --head
```

### 4.2 Login padrão
- URL: `http://localhost:3000/login`
- Usuário: `admin@padaria.com`
- Senha: `admin123`

### 4.3 Testes funcionais rápidos
- Dashboard de Auditoria (rota `/auditoria`) exibe métricas e gráficos.
- Portal de Direitos (rota `/portal-direitos`) responde sem autenticação.
- Endpoint `/api/dashboard/auditoria/metricas-gerais` retorna dados em JSON.

---

## 5. Finalização dos serviços
- Pressione `Ctrl+C` em cada terminal para desligar processos manuais.
- No Windows, execute `.\stop_system.bat` para encerrar os serviços iniciados pelo script.
- Limpe caches temporários com `npm cache clean --force` e `mvn clean` quando necessário.

---

## 6. Troubleshooting avançado

| Cenário | Diagnóstico | Ação |
| --- | --- | --- |
| Backend não sobe | Verifique logs em `synvia-core/target/spring.log` | Confirme versão do Java e credenciais de banco. |
| Erros CORS | Confira `FrontGoDgital/src/services/api.js` e `synvia-core` -> `WebSecurityConfig` | Alinhe as origens permitidas. |
| IA sem cache | Confirme disponibilidade do Redis (opcional) ou utilize modo fallback | Ajuste `REDIS_URL` ou desabilite temporariamente. |
| HTTPS falha | Certifique-se de que `keystore.p12` está acessível e senha correta | Regere certificados com `generate_ssl_certs.sh` se necessário. |

---

## 7. Checklist integrado de validação
```bash
pytest -q                      # Testes rápidos do módulo de IA
mvn clean verify               # Backend com build + testes
npm run lint && npm test       # Qualidade e testes do frontend
docker compose up -d          # Execução integrada com chaves LLM de sandbox
```

> Execute os comandos após alterações relevantes ou antes de homologações.

## 8. Referências
- [Início rápido](INICIO_RAPIDO.md)
- [Documentação técnica consolidada](../technical/DOCUMENTACAO_TECNICA_COMPLETA.md)
- [Roadmap estratégico e próximos passos](../ROADMAP_TRANSFORMACAO_DIGITAL.md)

> Última revisão: dezembro/2025
