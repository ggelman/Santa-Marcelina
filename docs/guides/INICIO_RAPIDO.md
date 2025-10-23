﻿# âš¡ InÃ­cio RÃ¡pido (â‰¤ 5 minutos)

Guia objetivo para subir o Synvia localmente. Ideal para demonstraÃ§Ãµes ou validaÃ§Ãµes rÃ¡pidas apÃ³s um clone do repositÃ³rio.

---

## âœ… PrÃ©-requisitos mÃ­nimos
- Java 17+ com Maven configurado no `PATH`.
- Node.js 18+ com `npm`.
- Python 3.10+.
- Certificados SSL jÃ¡ presentes em `ssl_certificates/` (incluÃ­dos no repositÃ³rio).

---

## ðŸš€ ExecuÃ§Ã£o automatizada (Windows)
1. Abra um **PowerShell** na raiz do repositÃ³rio.
2. Execute:
   ```powershell
   .\start_system.bat
   ```
   > Execute em PowerShell ou Prompt de Comando (evite Git Bash) para que os utilitários nativos do Windows funcionem corretamente.
3. Aguarde a inicializaÃ§Ã£o (â‰ˆ 2 minutos). O script inicia backend, frontend e mÃ³dulo de IA.
4. Acesse o frontend em `http://localhost:3000`.

Para encerrar todos os serviÃ§os use:
```powershell
.\stop_system.bat
```

---

## ðŸ§­ ExecuÃ§Ã£o manual (Linux/macOS/Windows)
Em trÃªs terminais separados, execute os comandos abaixo a partir da raiz do projeto.

### 1. MÃ³dulo de IA (porta 5001 HTTP)
```bash
cd ai_module
python -m venv .venv && source .venv/bin/activate  # opcional
# .venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
export USE_HTTPS=false  # PowerShell: $env:USE_HTTPS="false"
python ai_service.py
```
> Para executar em HTTPS defina `USE_HTTPS=true`, utilize os certificados de `../ssl_certificates` e a porta passarÃ¡ a ser `5443`.

### 2. Backend Spring Boot (porta 8080)
```bash
cd synvia-core
mvn spring-boot:run
```

### 3. Frontend React (porta 3000)
```bash
cd FrontGoDgital
npm install
npm start
```

---

## ðŸ” VerificaÃ§Ãµes rÃ¡pidas
- **Frontend:** `http://localhost:3000` deve exibir a tela de login.
- **Backend:** `http://localhost:8080/actuator/health` retorna `{"status":"UP"}`.
- **IA:** `http://localhost:5001/health` retorna `{"status":"ok"}`. Para HTTPS utilize `https://localhost:5443/health`.

Use `system_status.bat` (Windows) ou `ps`/`lsof -i` (Linux/macOS) para confirmar as portas ativas.

---

## âœ… ValidaÃ§Ã£o expressa pÃ³s-start
```bash
pytest -q                      # Testes rÃ¡pidos do mÃ³dulo de IA
mvn clean verify               # Backend com build + testes
npm run lint && npm test       # Qualidade e testes do frontend
```

> Para execuÃ§Ã£o integrada (IA + backend + frontend) utilize `docker compose up -d` com chaves LLM de sandbox configuradas.

---

## ðŸ› ï¸ Problemas frequentes
| Sintoma | AÃ§Ã£o recomendada |
| --- | --- |
| Porta em uso | Finalize processos anteriores (`stop_system.bat` ou `lsof -ti:3000 -sTCP:LISTEN`). |
| Erro de dependÃªncia Node | Execute `npm install --legacy-peer-deps` e repita `npm start`. |
| Maven nÃ£o encontra o JDK | Garanta `JAVA_HOME` apontando para uma instalaÃ§Ã£o Java 17+. |
| AI Service falha ao iniciar | Verifique certificados em `ssl_certificates/` ou execute com `USE_HTTPS=false`. |

---

## ðŸ“Ž PrÃ³ximos passos
- Consulte o [guia completo de execuÃ§Ã£o](GUIA_EXECUCAO_COMPLETO.md) para detalhes de certificados, perfis HTTPS e testes.
- Acompanhe o estado do projeto e o plano evolutivo no [roadmap estratÃ©gico](../roadmap/ROADMAP_SYNVIA.md).

> Tempo mÃ©dio para o primeiro acesso: **â‰ˆ 5 minutos**
>
> Ãšltima atualizaÃ§Ã£o: outubro/2025



