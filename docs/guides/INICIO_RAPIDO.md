# ⚡ INÍCIO RÁPIDO - 5 Minutos

> Como rodar o sistema completo em **5 minutos**

---

## 🚀 EXECUÇÃO AUTOMÁTICA

### 1️⃣ **Abrir Terminal**
```batch
cd C:\projects\FIAP\Fase6\SRC
```

### 2️⃣ **Executar Script**
```batch
.\start_all_services_correto.bat
```

### 3️⃣ **Aguardar Inicialização**
- ⏳ AI Service (30s)
- ⏳ Backend (60s) 
- ⏳ Frontend (30s)

### 4️⃣ **Acessar Sistema**
- 🌐 **URL:** http://localhost:3000
- 👤 **Login:** admin@padaria.com
- 🔑 **Senha:** admin123

---

## ✅ VERIFICAÇÃO RÁPIDA

### 🔍 **Portas Ativas**
```batch
netstat -an | findstr ":3000 :8443 :5443"
```

**Resultado esperado:**
```
:3000  ✅ Frontend
:8443  ✅ Backend HTTPS  
:5443  ✅ AI Service
```

### 🧪 **Teste Funcional**
1. **Login** → Dashboard carrega
2. **Menu lateral** → Todas opções visíveis
3. **Monitor de Segurança** → Status verde
4. **Nova Venda** → Formulário funciona

---

## ❌ PROBLEMAS COMUNS

| Erro | Solução |
|------|---------|
| `Erro: Diretório não encontrado` | Verifique se está na pasta correta: `C:\projects\FIAP\Fase6\SRC` |
| `Porta já em uso` | Execute: `stop_all_services.bat` |
| `Status Desconhecido` | Aguarde 2 minutos ou aceite certificado SSL |
| `Login falha` | Verifique se backend está rodando (porta 8443) |

---

## 🛑 PARAR SISTEMA

```batch
.\stop_all_services.bat
```

ou **Ctrl+C** em cada terminal

---

## 📚 PRÓXIMOS PASSOS

- 📖 **README.md** → Visão geral completa
- 🧪 **CHECKLIST_TESTE.md** → Validação completa
- 🔧 **SOLUCAO_PROBLEMAS.md** → Problemas específicos

---

**⏱️ Tempo total: ~5 minutos | 🎯 Taxa de sucesso: 95%**