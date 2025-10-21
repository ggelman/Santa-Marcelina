# ⚡ Início Rápido (≤ 5 minutos)

Guia objetivo para subir o goDigital Code localmente. Ideal para demonstrações ou validações rápidas após um clone do repositório.

---

## ✅ Pré-requisitos mínimos
- Java 17+ com Maven configurado no `PATH`.
- Node.js 18+ com `npm`.
- Python 3.10+.
- Certificados SSL já presentes em `ssl_certificates/` (incluídos no repositório).

---

## 🚀 Execução automatizada (Windows)
1. Abra um **PowerShell** na raiz do repositório.
2. Execute:
   ```powershell
   .\start_system.bat
   ```
3. Aguarde a inicialização (≈ 2 minutos). O script inicia backend, frontend e módulo de IA.
4. Acesse o frontend em `http://localhost:3000`.

Para encerrar todos os serviços use:
```powershell
.\stop_system.bat
```

---

## 🧭 Execução manual (Linux/macOS/Windows)
Em três terminais separados, execute os comandos abaixo a partir da raiz do projeto.

### 1. Módulo de IA (porta 5443 HTTPS)
```bash
cd ai_module
python -m venv .venv && source .venv/bin/activate  # opcional
# .venv\\Scripts\\activate  # Windows PowerShell
pip install -r requirements.txt
python ai_service.py  # usa certificados de ../ssl_certificates
```
> Para executar em HTTP utilize `USE_HTTPS=false python ai_service.py` (porta 5001).

### 2. Backend Spring Boot (porta 8080)
```bash
cd padariaApi
mvn spring-boot:run
```

### 3. Frontend React (porta 3000)
```bash
cd FrontGoDgital
npm install
npm start
```

---

## 🔍 Verificações rápidas
- **Frontend:** `http://localhost:3000` deve exibir a tela de login.
- **Backend:** `http://localhost:8080/actuator/health` retorna `{"status":"UP"}`.
- **IA:** `https://localhost:5443/health` retorna `{"status":"ok"}` (aceite o certificado autoassinado). Em HTTP utilize `http://localhost:5001/health`.

Use `system_status.bat` (Windows) ou `ps`/`lsof -i` (Linux/macOS) para confirmar as portas ativas.

---

## ✅ Validação expressa pós-start
```bash
pytest -q                      # Testes rápidos do módulo de IA
mvn clean verify               # Backend com build + testes
npm run lint && npm test       # Qualidade e testes do frontend
```

> Para execução integrada (IA + backend + frontend) utilize `docker compose up -d` com chaves LLM de sandbox configuradas.

---

## 🛠️ Problemas frequentes
| Sintoma | Ação recomendada |
| --- | --- |
| Porta em uso | Finalize processos anteriores (`stop_system.bat` ou `lsof -ti:3000 -sTCP:LISTEN`). |
| Erro de dependência Node | Execute `npm install --legacy-peer-deps` e repita `npm start`. |
| Maven não encontra o JDK | Garanta `JAVA_HOME` apontando para uma instalação Java 17+. |
| AI Service falha ao iniciar | Verifique certificados em `ssl_certificates/` ou execute com `USE_HTTPS=false`. |

---

## 📎 Próximos passos
- Consulte o [guia completo de execução](GUIA_EXECUCAO_COMPLETO.md) para detalhes de certificados, perfis HTTPS e testes.
- Acompanhe o estado do projeto e o plano evolutivo no [roadmap estratégico](../ROADMAP_TRANSFORMACAO_DIGITAL.md).

> Tempo médio para o primeiro acesso: **≈ 5 minutos**
>
> Última atualização: dezembro/2025
